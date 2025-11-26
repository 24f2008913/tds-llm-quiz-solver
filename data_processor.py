"""
Data Processor - Handles various data processing tasks
"""
import os
import logging
import pandas as pd
import numpy as np
from typing import Any, Dict, List, Optional, Union
import requests
from io import BytesIO
import base64
import json

logger = logging.getLogger(__name__)


class DataProcessor:
    """Handles data processing for various formats"""
    
    def __init__(self):
        self.download_dir = os.path.join(os.getcwd(), 'downloads')
        os.makedirs(self.download_dir, exist_ok=True)
    
    def download_file(self, url: str, filename: Optional[str] = None) -> str:
        """
        Download a file from URL
        
        Args:
            url: URL to download from
            filename: Optional filename (will be auto-generated if not provided)
        
        Returns:
            Path to downloaded file
        """
        try:
            logger.info(f"Downloading file from: {url}")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            if not filename:
                # Try to get filename from URL or headers
                from urllib.parse import urlparse
                parsed = urlparse(url)
                filename = os.path.basename(parsed.path) or 'downloaded_file'
            
            filepath = os.path.join(self.download_dir, filename)
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"File downloaded to: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error downloading file: {str(e)}")
            raise
    
    def process_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        Process PDF file and extract data
        
        Args:
            pdf_path: Path to PDF file
        
        Returns:
            Dict with text, tables, and metadata
        """
        try:
            import pdfplumber
            
            result = {
                'text': '',
                'tables': [],
                'pages': []
            }
            
            with pdfplumber.open(pdf_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    page_data = {
                        'page_number': i + 1,
                        'text': page.extract_text() or '',
                        'tables': []
                    }
                    
                    # Extract tables
                    tables = page.extract_tables()
                    for table in tables:
                        if table:
                            # Convert to DataFrame for easier processing
                            df = pd.DataFrame(table[1:], columns=table[0])
                            page_data['tables'].append(df)
                            result['tables'].append({
                                'page': i + 1,
                                'data': df
                            })
                    
                    result['pages'].append(page_data)
                    result['text'] += page_data['text'] + '\n\n'
            
            logger.info(f"Processed PDF: {len(result['pages'])} pages, {len(result['tables'])} tables")
            return result
            
        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}")
            raise
    
    def process_csv(self, csv_path: str) -> pd.DataFrame:
        """
        Process CSV file
        
        Args:
            csv_path: Path to CSV file
        
        Returns:
            DataFrame
        """
        try:
            df = pd.read_csv(csv_path)
            logger.info(f"Processed CSV: {df.shape[0]} rows, {df.shape[1]} columns")
            return df
        except Exception as e:
            logger.error(f"Error processing CSV: {str(e)}")
            raise
    
    def process_excel(self, excel_path: str, sheet_name: Optional[str] = None) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
        """
        Process Excel file
        
        Args:
            excel_path: Path to Excel file
            sheet_name: Specific sheet to read (None = all sheets)
        
        Returns:
            DataFrame or dict of DataFrames
        """
        try:
            if sheet_name:
                df = pd.read_excel(excel_path, sheet_name=sheet_name)
                logger.info(f"Processed Excel sheet '{sheet_name}': {df.shape[0]} rows, {df.shape[1]} columns")
                return df
            else:
                dfs = pd.read_excel(excel_path, sheet_name=None)
                logger.info(f"Processed Excel: {len(dfs)} sheets")
                return dfs
        except Exception as e:
            logger.error(f"Error processing Excel: {str(e)}")
            raise
    
    def process_json(self, json_path: str) -> Any:
        """
        Process JSON file
        
        Args:
            json_path: Path to JSON file
        
        Returns:
            Parsed JSON data
        """
        try:
            with open(json_path, 'r') as f:
                data = json.load(f)
            logger.info(f"Processed JSON file")
            return data
        except Exception as e:
            logger.error(f"Error processing JSON: {str(e)}")
            raise
    
    def analyze_dataframe(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Perform basic analysis on DataFrame
        
        Args:
            df: DataFrame to analyze
        
        Returns:
            Analysis summary
        """
        analysis = {
            'shape': df.shape,
            'columns': df.columns.tolist(),
            'dtypes': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'summary_stats': df.describe().to_dict(),
            'head': df.head().to_dict(),
        }
        
        return analysis
    
    def create_visualization(
        self,
        df: pd.DataFrame,
        chart_type: str,
        x: Optional[str] = None,
        y: Optional[str] = None,
        title: str = "Chart",
        save_path: Optional[str] = None
    ) -> str:
        """
        Create a visualization from data
        
        Args:
            df: DataFrame with data
            chart_type: Type of chart (bar, line, scatter, pie, etc.)
            x: Column for x-axis
            y: Column for y-axis
            title: Chart title
            save_path: Path to save chart
        
        Returns:
            Path to saved chart or base64 encoded image
        """
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        try:
            plt.figure(figsize=(10, 6))
            
            if chart_type == 'bar':
                if x and y:
                    df.plot(kind='bar', x=x, y=y, title=title)
                else:
                    df.plot(kind='bar', title=title)
            elif chart_type == 'line':
                if x and y:
                    df.plot(kind='line', x=x, y=y, title=title)
                else:
                    df.plot(kind='line', title=title)
            elif chart_type == 'scatter':
                if x and y:
                    plt.scatter(df[x], df[y])
                    plt.xlabel(x)
                    plt.ylabel(y)
                    plt.title(title)
            elif chart_type == 'pie':
                if x and y:
                    df.set_index(x)[y].plot(kind='pie', title=title, autopct='%1.1f%%')
                else:
                    df.iloc[:, 0].value_counts().plot(kind='pie', title=title, autopct='%1.1f%%')
            elif chart_type == 'hist':
                if x:
                    df[x].hist(bins=20)
                    plt.xlabel(x)
                    plt.title(title)
                else:
                    df.hist()
                    plt.title(title)
            
            plt.tight_layout()
            
            if not save_path:
                save_path = os.path.join(self.download_dir, 'chart.png')
            
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Chart saved to: {save_path}")
            return save_path
            
        except Exception as e:
            logger.error(f"Error creating visualization: {str(e)}")
            raise
    
    def image_to_base64(self, image_path: str) -> str:
        """
        Convert image to base64 data URI
        
        Args:
            image_path: Path to image file
        
        Returns:
            Base64 data URI
        """
        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            encoded = base64.b64encode(image_data).decode('utf-8')
            
            # Determine MIME type from extension
            ext = os.path.splitext(image_path)[1].lower()
            mime_types = {
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.gif': 'image/gif',
                '.svg': 'image/svg+xml'
            }
            mime_type = mime_types.get(ext, 'image/png')
            
            data_uri = f"data:{mime_type};base64,{encoded}"
            return data_uri
            
        except Exception as e:
            logger.error(f"Error converting image to base64: {str(e)}")
            raise
    
    def scrape_webpage(self, url: str) -> Dict[str, Any]:
        """
        Scrape data from a webpage
        
        Args:
            url: URL to scrape
        
        Returns:
            Scraped data
        """
        from bs4 import BeautifulSoup
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract tables
            tables = []
            for table in soup.find_all('table'):
                df = pd.read_html(str(table))[0]
                tables.append(df)
            
            result = {
                'text': soup.get_text(strip=True),
                'tables': tables,
                'title': soup.title.string if soup.title else '',
                'links': [{'url': a.get('href'), 'text': a.get_text(strip=True)} 
                         for a in soup.find_all('a', href=True)]
            }
            
            logger.info(f"Scraped webpage: {len(tables)} tables, {len(result['links'])} links")
            return result
            
        except Exception as e:
            logger.error(f"Error scraping webpage: {str(e)}")
            raise
