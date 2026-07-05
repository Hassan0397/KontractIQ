from setuptools import setup, find_packages

setup(
    name="kontractiq",
    version="1.0.0",
    description="AI-Powered Contract Intelligence Platform",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "streamlit==1.32.0",
        "pandas==2.0.3",
        "numpy==1.24.3",
        "plotly==5.18.0",
        "PyPDF2==3.0.1",
        "pdfplumber==0.10.3",
        "python-docx==1.1.0",
        "scikit-learn==1.3.2",
        "rank-bm25==0.2.2",
        "spacy==3.7.2",
        "reportlab==4.0.7",
        "jinja2==3.1.2",
        "python-dotenv==1.0.0"
    ],
    python_requires=">=3.10",
)