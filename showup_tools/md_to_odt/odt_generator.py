"""
ODT Generator Module

This module handles the conversion of Markdown content to ODT format
with properly embedded images.
"""

import os
import re
import logging
import markdown
from pathlib import Path
import tempfile
import shutil
import html
import subprocess

# ODT generation using odfpy
from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties, ParagraphProperties, GraphicProperties
from odf.text import P, H, Span, A, ListItem, List
from odf.draw import Frame, Image as DrawImage
from PIL import Image as PILImage

logger = logging.getLogger('md_to_odt.odt_generator')

class ODTGenerator:
    """Class for generating ODT files from Markdown content with embedded images"""
    
    def __init__(self):
        """Initialize the ODT generator"""
        self.logger = logging.getLogger('md_to_odt.odt_generator')
        self.picture_counter = 1
    
    def generate_odt(self, markdown_file, selected_images, output_file):
        """
        Generate an ODT file from a Markdown file with embedded images
        using pandoc or direct ODT generation as fallback
        
        Args:
            markdown_file: Path to the Markdown file
            selected_images: Dictionary mapping references to selected images
            output_file: Path to save the ODT file
        """
        self.logger.info(f"Generating ODT file: {output_file}")
        
        try:
            # Create a temporary directory
            temp_dir = tempfile.mkdtemp()
            self.logger.info(f"Created temporary directory: {temp_dir}")
            
            try:
                # Organize images and get updated markdown
                processed_markdown, image_dir, organized_images = self._organize_images_and_prepare_markdown(
                    markdown_file, selected_images, temp_dir
                )
                
                # Write updated markdown to temp file
                temp_markdown = os.path.join(temp_dir, "processed.md")
                with open(temp_markdown, 'w', encoding='utf-8') as f:
                    f.write(processed_markdown)
                
                # Create output directory if it doesn't exist
                output_path = Path(output_file)
                output_path.parent.mkdir(exist_ok=True, parents=True)
                
                # Try to convert with pandoc first
                try:
                    self._convert_with_pandoc(temp_markdown, output_file, image_dir)
                    self.logger.info(f"ODT file generated successfully with Pandoc: {output_file}")
                except Exception as pandoc_error:
                    self.logger.warning(f"Pandoc conversion failed: {str(pandoc_error)}")
                    self.logger.info("Falling back to direct ODT generation")
                    # Use direct ODT generation as fallback
                    self._generate_odt_directly(processed_markdown, organized_images, output_file)
                    self.logger.info(f"ODT file generated successfully with direct method: {output_file}")
                
            finally:
                # Clean up temporary directory
                shutil.rmtree(temp_dir, ignore_errors=True)
                self.logger.info(f"Cleaned up temporary directory: {temp_dir}")
        
        except Exception as e:
            self.logger.error(f"Error generating ODT file: {str(e)}")
            raise
    
    def _organize_images_and_prepare_markdown(self, markdown_file, selected_images, temp_dir):
        """
        Organize images and update markdown references
        
        Args:
            markdown_file: Path to the Markdown file
            selected_images: Dictionary mapping references to selected images
            temp_dir: Path to the temporary directory
            
        Returns:
            Tuple of (processed_markdown, image_dir, organized_images)
        """
        # Extract lesson number from markdown file path
        markdown_path = Path(markdown_file)
        lesson_match = re.search(r'lesson\s*(\d+)', str(markdown_path), re.IGNORECASE)
        lesson_number = lesson_match.group(1) if lesson_match else "unknown"
        
        # Create lesson directory if it doesn't exist
        output_dir = markdown_path.parent / f"odt_images_lesson{lesson_number}"
        output_dir.mkdir(exist_ok=True)
        
        # Create images directory in temp dir
        image_dir = os.path.join(temp_dir, "images")
        os.makedirs(image_dir, exist_ok=True)
        
        # Read the original markdown content
        with open(markdown_file, 'r', encoding='utf-8') as file:
            markdown_content = file.read()
        
        # Dictionary to store images with paths
        organized_images = {}
        
        # Process each image and update markdown references
        for reference, image in selected_images.items():
            if not image:
                continue
                
            try:
                # Get source image path
                source_path = Path(image.image_path)
                
                # Create temp copy for processing
                img_filename = source_path.name
                temp_image_path = os.path.join(image_dir, img_filename)
                
                # Optimize image if needed
                with PILImage.open(source_path) as img:
                    # Check if image is large and needs optimization
                    if img.width > 2000 or img.height > 2000:
                        # Create a resized version
                        max_dim = 1500  # Reasonable size for document
                        if img.width > img.height:
                            new_width = max_dim
                            new_height = int(img.height * (max_dim / img.width))
                        else:
                            new_height = max_dim
                            new_width = int(img.width * (max_dim / img.height))
                        
                        # Resize and save
                        resized_img = img.resize((new_width, new_height), PILImage.LANCZOS)
                        resized_img.save(temp_image_path, quality=90)
                    else:
                        # Just copy the file
                        shutil.copy2(source_path, temp_image_path)
                
                # Destination path for final organization
                dest_path = output_dir / source_path.name
                
                # Move the original file if it's not already in the target directory
                if source_path != dest_path:
                    try:
                        # Move the file (not copy)
                        shutil.move(str(source_path), str(dest_path))
                        self.logger.info(f"Moved image {source_path} to {dest_path}")
                    except Exception as e:
                        self.logger.warning(f"Error moving image {source_path} to {dest_path}: {str(e)}")
                        # Fallback to copy if move fails
                        if not dest_path.exists():
                            shutil.copy2(str(source_path), str(dest_path))
                
                # Create caption text
                caption_text = ""
                
                # Add figure number
                figure_num = reference.figure_number or ""
                if figure_num:
                    # Extract just the number from "Fig X"
                    fig_num_match = re.search(r'\d+', figure_num)
                    if fig_num_match:
                        fig_num = fig_num_match.group(0)
                        caption_text += f"Fig.{fig_num} "
                
                # Add metadata
                metadata = image.metadata
                if 'photographer' in metadata:
                    caption_text += f"({metadata['photographer']} on [Pexels](https://www.pexels.com), "
                    if 'year' in metadata:
                        caption_text += metadata['year']
                    else:
                        caption_text += "N.d"
                    caption_text += ") "
                
                # Add caption text
                caption_content = reference.modified_caption or reference.caption or reference.description
                if caption_content:
                    caption_text += caption_content
                
                # Save image info for direct ODT generation
                organized_images[reference] = {
                    'temp_path': temp_image_path,
                    'caption': caption_text,
                    'reference': reference,
                    'metadata': metadata,
                    'dest_path': dest_path
                }
                
                # Replace the image reference with markdown image syntax for pandoc
                relative_path = os.path.join("images", img_filename)
                image_markdown = f"\n\n![{caption_text}]({relative_path})\n\n"
                
                # Replace the original reference with new markdown
                markdown_content = markdown_content.replace(reference.reference_text, image_markdown)
                
            except Exception as e:
                self.logger.error(f"Error processing image {image.image_path}: {str(e)}")
                # Replace with error text if processing fails
                markdown_content = markdown_content.replace(
                    reference.reference_text, 
                    "\n\n[Image processing failed]\n\n"
                )
        
        return markdown_content, image_dir, organized_images
    
    def _convert_with_pandoc(self, markdown_file, output_file, image_dir):
        """
        Convert markdown to ODT using pandoc
        
        Args:
            markdown_file: Path to the markdown file
            output_file: Path to the output ODT file
            image_dir: Path to the directory containing images
        """
        try:
            # Check if pandoc is installed
            try:
                # Try to run pandoc --version
                subprocess.run(["pandoc", "--version"], check=True, capture_output=True)
                self.logger.info("Found pandoc installed on the system")
            except (subprocess.SubprocessError, FileNotFoundError):
                # If pandoc is not in PATH, we need to use pypandoc
                self.logger.warning("Pandoc not found in PATH, trying with pypandoc")
                self._convert_with_pypandoc(markdown_file, output_file, image_dir)
                return
            
            # Construct the pandoc command
            command = [
                "pandoc",
                markdown_file,
                "-o", output_file,
                "--resource-path", os.path.dirname(markdown_file),
                "--resource-path", image_dir,
                "--standalone",
                "--embed-resources"
            ]
            
            # Run pandoc
            self.logger.info(f"Running pandoc: {' '.join(command)}")
            process = subprocess.run(command, check=True, capture_output=True, text=True)
            
            # Log output for debugging
            if process.stdout:
                self.logger.info(f"Pandoc stdout: {process.stdout}")
            if process.stderr:
                self.logger.warning(f"Pandoc stderr: {process.stderr}")
                
        except Exception as e:
            self.logger.error(f"Error running pandoc: {str(e)}")
            # Try pypandoc as fallback
            self.logger.info("Trying pypandoc as fallback")
            self._convert_with_pypandoc(markdown_file, output_file, image_dir)
    
    def _convert_with_pypandoc(self, markdown_file, output_file, image_dir):
        """
        Convert markdown to ODT using pypandoc
        
        Args:
            markdown_file: Path to the markdown file
            output_file: Path to the output ODT file
            image_dir: Path to the directory containing images
        """
        try:
            # Import pypandoc
            import pypandoc
            
            # Convert using pypandoc
            self.logger.info(f"Converting with pypandoc: {markdown_file} -> {output_file}")
            
            # Set the resource path for images
            filters = []
            extra_args = [
                '--resource-path', os.path.dirname(markdown_file),
                '--resource-path', image_dir,
                '--standalone',
                '--embed-resources'
            ]
            
            # Perform the conversion
            output = pypandoc.convert_file(
                source_file=markdown_file,
                format="markdown",
                to="odt",
                outputfile=output_file,
                filters=filters,
                extra_args=extra_args
            )
            
            # Check for output
            if output:
                self.logger.info(f"Pypandoc output: {output}")
                
        except ImportError:
            self.logger.error("Could not import pypandoc. Please install it with: pip install pypandoc")
            raise
        except Exception as e:
            self.logger.error(f"Error in pypandoc conversion: {str(e)}")
            raise
    
    def _generate_odt_directly(self, markdown_content, organized_images, output_file):
        """
        Generate ODT file directly using odfpy
        
        Args:
            markdown_content: Markdown content as string
            organized_images: Dictionary mapping references to image info
            output_file: Path to the output ODT file
        """
        # Create ODT document
        doc = OpenDocumentText()
        self._add_styles(doc)
        
        # Convert markdown to HTML for easier processing
        html_content = markdown.markdown(
            markdown_content, 
            extensions=['tables', 'fenced_code', 'nl2br']
        )
        
        # Process HTML content and add to document
        self._add_content_to_document(doc, html_content)
        
        # Add images to document
        for ref, img_info in organized_images.items():
            self._add_image_with_caption(doc, img_info)
        
        # Save document
        doc.save(output_file)
    
    def _add_content_to_document(self, doc, html_content):
        """
        Add HTML content to the document
        
        Args:
            doc: OpenDocumentText instance
            html_content: HTML content as string
        """
        # Split HTML by main elements for better processing
        elements = re.split(r'(<h[1-6][^>]*>.*?</h[1-6]>|<p>.*?</p>|<ul>.*?</ul>|<ol>.*?</ol>|<li>.*?</li>|<blockquote>.*?</blockquote>)', html_content, flags=re.DOTALL)
        
        for element in elements:
            if not element or element.isspace():
                continue
                
            # Check for headings
            heading_match = re.match(r'<h([1-6])[^>]*>(.*?)</h\1>', element, re.DOTALL)
            if heading_match:
                level = int(heading_match.group(1))
                text = self._process_inline_formatting(heading_match.group(2))
                heading = H(outlinelevel=level, stylename=f"Heading{level}")
                self._add_text_with_formatting(heading, text)
                doc.text.addElement(heading)
                continue
            
            # Check for paragraphs
            paragraph_match = re.match(r'<p>(.*?)</p>', element, re.DOTALL)
            if paragraph_match:
                paragraph_content = paragraph_match.group(1)
                
                # Skip image references, we'll handle them separately
                if '![' in paragraph_content and '](' in paragraph_content:
                    continue
                
                # Regular paragraph
                p = P(stylename="Normal")
                self._add_text_with_formatting(p, self._process_inline_formatting(paragraph_content))
                doc.text.addElement(p)
                continue
            
            # Check for unordered lists
            if element.startswith('<ul>') and element.endswith('</ul>'):
                list_content = re.sub(r'</?ul>', '', element)
                list_items = re.findall(r'<li>(.*?)</li>', list_content, re.DOTALL)
                
                # Create list
                odt_list = List(stylename="ListItem")
                
                # Add list items
                for item_content in list_items:
                    list_item = ListItem()
                    p = P(stylename="ListItem")
                    self._add_text_with_formatting(p, self._process_inline_formatting(item_content))
                    list_item.addElement(p)
                    odt_list.addElement(list_item)
                
                doc.text.addElement(odt_list)
                continue
            
            # Check for ordered lists
            if element.startswith('<ol>') and element.endswith('</ol>'):
                list_content = re.sub(r'</?ol>', '', element)
                list_items = re.findall(r'<li>(.*?)</li>', list_content, re.DOTALL)
                
                # Create list
                odt_list = List(stylename="ListItem")
                
                # Add list items
                for i, item_content in enumerate(list_items, 1):
                    list_item = ListItem()
                    p = P(stylename="ListItem")
                    # Add number prefix
                    p.addText(f"{i}. ")
                    self._add_text_with_formatting(p, self._process_inline_formatting(item_content))
                    list_item.addElement(p)
                    odt_list.addElement(list_item)
                
                doc.text.addElement(odt_list)
                continue
            
            # Check for blockquotes
            if element.startswith('<blockquote>') and element.endswith('</blockquote>'):
                blockquote_content = re.sub(r'</?blockquote>', '', element)
                
                # Process blockquote content
                p = P(stylename="Normal")
                blockquote_text = "> " + blockquote_content.strip().replace('\n', '\n> ')
                self._add_text_with_formatting(p, self._process_inline_formatting(blockquote_text))
                doc.text.addElement(p)
                continue
    
    def _process_inline_formatting(self, html_content):
        """
        Process inline HTML formatting to preserve styles
        
        Args:
            html_content: HTML content with inline formatting
            
        Returns:
            Processed content with formatting markers
        """
        # Process strong/bold text
        html_content = re.sub(r'<(?:strong|b)>(.*?)</(?:strong|b)>', r'**\1**', html_content, flags=re.DOTALL)
        
        # Process em/italic text
        html_content = re.sub(r'<(?:em|i)>(.*?)</(?:em|i)>', r'*\1*', html_content, flags=re.DOTALL)
        
        # Process links
        html_content = re.sub(r'<a href="([^"]+)">(.*?)</a>', r'[\2](\1)', html_content, flags=re.DOTALL)
        
        # Remove other tags
        html_content = re.sub(r'<[^>]+>', '', html_content)
        
        # Decode HTML entities
        html_content = html.unescape(html_content)
        
        return html_content
    
    def _add_image_with_caption(self, doc, img_info):
        """
        Add image with caption to the document
        
        Args:
            doc: OpenDocumentText instance
            img_info: Dictionary with image information
        """
        try:
            # Get image info
            image_path = img_info['temp_path']
            caption = img_info['caption']
            
            # Calculate image dimensions
            with PILImage.open(image_path) as img:
                img_width, img_height = img.size
            
            # Scale image to fit in the document (max width: 16cm)
            max_width_cm = 16
            width_cm = min(max_width_cm, 16)
            height_cm = width_cm * (img_height / img_width)
            
            # Create a unique name for this image
            image_name = f"Image{self.picture_counter}"
            self.picture_counter += 1
            
            # Add image to document
            p = P(stylename="Normal")
            frame = Frame(
                stylename="ImageFrame",
                width=f"{width_cm:.2f}cm",
                height=f"{height_cm:.2f}cm",
                anchortype="paragraph"
            )
            
            # Add image to frame
            href = doc.addPicture(image_path)
            draw_image = DrawImage(href=href)
            frame.addElement(draw_image)
            p.addElement(frame)
            doc.text.addElement(p)
            
            # Add caption paragraph
            caption_p = P(stylename="FigureCaption")
            
            # Process caption to handle links
            self._add_caption_with_links(caption_p, caption)
            
            doc.text.addElement(caption_p)
            
        except Exception as e:
            self.logger.error(f"Error adding image to document: {str(e)}")
            
            # Add error message as fallback
            p = P(stylename="Normal")
            p.addText("⚠️ [Image Embedding Failed] ⚠️")
            doc.text.addElement(p)
            
            caption_p = P(stylename="FigureCaption")
            caption_p.addText(caption)
            doc.text.addElement(caption_p)
    
    def _add_caption_with_links(self, paragraph, caption_text):
        """
        Add caption text with proper links to a paragraph
        
        Args:
            paragraph: ODT paragraph element
            caption_text: Caption text with markdown-style links
        """
        # Process links in the caption
        link_pattern = r'\[(.*?)\]\((.*?)\)'
        parts = re.split(f'({link_pattern})', caption_text)
        
        for part in parts:
            # Check if this part is a link
            link_match = re.match(link_pattern, part)
            if link_match:
                link_text = link_match.group(1)
                link_url = link_match.group(2)
                
                # Create hyperlink
                link = A(href=link_url, stylename="Hyperlink")
                link.addText(link_text)
                paragraph.addElement(link)
            else:
                # Regular text
                if part:
                    paragraph.addText(part)
    
    def _add_styles(self, doc):
        """
        Add required styles to the ODT document
        
        Args:
            doc: OpenDocumentText instance
        """
        # Heading styles
        for level in range(1, 7):
            heading_style = Style(name=f"Heading{level}", family="paragraph")
            heading_style.addElement(TextProperties(
                fontsize=f"{20-level*2}pt", 
                fontweight="bold"
            ))
            doc.styles.addElement(heading_style)
        
        # Normal paragraph style
        normal_style = Style(name="Normal", family="paragraph")
        normal_style.addElement(ParagraphProperties(margintop="0.4cm", marginbottom="0.4cm"))
        normal_style.addElement(TextProperties(fontsize="11pt"))
        doc.styles.addElement(normal_style)
        
        # Figure caption style
        caption_style = Style(name="FigureCaption", family="paragraph")
        caption_style.addElement(ParagraphProperties(margintop="0.2cm", marginbottom="0.5cm", textalign="center"))
        caption_style.addElement(TextProperties(fontsize="10pt", fontstyle="italic"))
        doc.styles.addElement(caption_style)
        
        # Hyperlink style
        hyperlink_style = Style(name="Hyperlink", family="text")
        hyperlink_style.addElement(TextProperties(color="#0000ff", textunderlinestyle="solid", textunderlinewidth="auto"))
        doc.styles.addElement(hyperlink_style)
        
        # Image frame style
        image_frame_style = Style(name="ImageFrame", family="graphic")
        image_frame_style.addElement(GraphicProperties(padding="0.1cm", border="none"))
        doc.styles.addElement(image_frame_style)
        
        # Bold text style
        bold_style = Style(name="Bold", family="text")
        bold_style.addElement(TextProperties(fontweight="bold"))
        doc.styles.addElement(bold_style)
        
        # Italic text style
        italic_style = Style(name="Italic", family="text")
        italic_style.addElement(TextProperties(fontstyle="italic"))
        doc.styles.addElement(italic_style)
        
        # List styles
        list_style = Style(name="ListItem", family="paragraph")
        list_style.addElement(ParagraphProperties(marginleft="1cm", margintop="0.2cm", marginbottom="0.2cm"))
        doc.styles.addElement(list_style)
    
    def _add_text_with_formatting(self, element, text):
        """
        Add text with formatting to an ODT element
        
        Args:
            element: ODT element to add text to
            text: Text with formatting markers
        """
        # Process text chunks with formatting
        chunks = []
        current_chunk = ''
        i = 0
        
        while i < len(text):
            # Check for bold
            if text[i:i+2] == '**' and i+2 < len(text):
                # Add current chunk if any
                if current_chunk:
                    chunks.append(('normal', current_chunk))
                    current_chunk = ''
                
                # Find end of bold
                end_bold = text.find('**', i+2)
                if end_bold != -1:
                    bold_text = text[i+2:end_bold]
                    chunks.append(('bold', bold_text))
                    i = end_bold + 2
                else:
                    # No end bold found, treat as normal text
                    current_chunk += '**'
                    i += 2
            
            # Check for italic
            elif text[i] == '*' and i+1 < len(text):
                # Add current chunk if any
                if current_chunk:
                    chunks.append(('normal', current_chunk))
                    current_chunk = ''
                
                # Find end of italic
                end_italic = text.find('*', i+1)
                if end_italic != -1:
                    italic_text = text[i+1:end_italic]
                    chunks.append(('italic', italic_text))
                    i = end_italic + 1
                else:
                    # No end italic found, treat as normal text
                    current_chunk += '*'
                    i += 1
            
            # Check for link
            elif text[i] == '[' and i+1 < len(text):
                # Find end of link text
                end_text = text.find(']', i+1)
                if end_text != -1 and end_text+1 < len(text) and text[end_text+1] == '(':
                    # Find end of link URL
                    end_url = text.find(')', end_text+2)
                    if end_url != -1:
                        # Add current chunk if any
                        if current_chunk:
                            chunks.append(('normal', current_chunk))
                            current_chunk = ''
                        
                        link_text = text[i+1:end_text]
                        link_url = text[end_text+2:end_url]
                        chunks.append(('link', (link_text, link_url)))
                        i = end_url + 1
                    else:
                        # No end URL found, treat as normal text
                        current_chunk += text[i]
                        i += 1
                else:
                    # Not a well-formed link, treat as normal text
                    current_chunk += text[i]
                    i += 1
            
            else:
                # Normal text
                current_chunk += text[i]
                i += 1
        
        # Add final chunk if any
        if current_chunk:
            chunks.append(('normal', current_chunk))
        
        # Add chunks to element
        for chunk_type, chunk_content in chunks:
            if chunk_type == 'normal':
                element.addText(chunk_content)
            elif chunk_type == 'bold':
                span = Span(stylename="Bold")
                span.addText(chunk_content)
                element.addElement(span)
            elif chunk_type == 'italic':
                span = Span(stylename="Italic")
                span.addText(chunk_content)
                element.addElement(span)
            elif chunk_type == 'link':
                link_text, link_url = chunk_content
                link = A(href=link_url, stylename="Hyperlink")
                link.addText(link_text)
                element.addElement(link)