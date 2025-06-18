from setuptools import setup

packages = [
    "showup_tools",
    "showup_tools.bryce_tts",
    "showup_tools.fitness_podcaster",
    "showup_tools.simplified_app",
    "showup_tools.simplified_app.rag_system",
    "showup_tools.Markdown_To_CSV_StepOutline.src",
    "showup_tools.Markdown_To_CSV_StepOutline.src.utils",
    "showup_tools.Markdown_To_CSV_StepOutline.src.core",
    "showup_tools.Markdown_To_CSV_StepOutline.src.gui",
    "showup_tools.md_to_odt",
    "showup_tools.gmail_chatbot.gmail_chatbot",
    "showup_tools.gmail_chatbot.gmail_chatbot.handlers",
    "showup_tools.gmail_chatbot.gmail_chatbot.app",
    "showup_tools.gmail_chatbot.gmail_chatbot.app.handlers",
    "showup_tools.gmail_chatbot.gmail_chatbot.vector_db",
    "showup_tools.gmail_chatbot.gmail_chatbot.gui",
    "showup_tools.five_whys_analyzer",
    "showup_tools.five_whys_analyzer.ui",
    "showup_tools.five_whys_analyzer.utils",
]

setup(
    name="showup_tools",
    version="0.1.0",
    description="Auxiliary ShowupSquared tools",
    packages=packages,
    package_dir={"showup_tools": "showup-tools"},
    python_requires=">=3.7",
)
