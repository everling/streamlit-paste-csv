from pathlib import Path
from typing import Optional
import streamlit as st
import streamlit.components.v1 as components
from dataclasses import dataclass
import pandas as pd
import io

frontend_dir = (Path(__file__).parent / "frontend").absolute()
_component_func = components.declare_component(
    "streamlit_paste_csv", path=str(frontend_dir)
)


@dataclass
class PasteResult:
    """Dataclass to store output of Javascript Component."""
    dataframe: pd.DataFrame = None


def _csv_to_dataframe(csv_string: str, separator: str) -> pd.DataFrame:
    """Convert CSV string to pandas DataFrame"""
    return pd.read_csv(io.StringIO(csv_string), sep=separator)


def paste_csv_button(
        label: str,
        separator: str = ",",
        text_color: Optional[str] = "#ffffff",
        background_color: Optional[str] = "#3498db",
        hover_background_color: Optional[str] = "#2980b9",
        key: Optional[str] = 'paste_button',
        errors: Optional[str] = 'ignore'
) -> PasteResult:
    """
    Create a button that can be used to paste CSV data from the clipboard.

    Parameters
    ----------
    label : str
        The label to display next to the component.
    separator : str, optional
        The separator used in the CSV data. Use '\\t' for tab-separated data (e.g., from Excel).
        Default is ','.
    text_color : str, optional
        The color of the text, by default "#ffffff"
    background_color : str, optional
        The background color of the button, by default "#3498db"
    hover_background_color : str, optional
        The background color of the button when hovered, by default "#2980b9"
    key : str, optional
        An optional string to use as the unique key for the widget. Defaults to 'paste_button'.
    errors: str {'raise', 'ignore'}, optional
        If 'raise', then invalid input will raise an exception.
        If 'ignore', then invalid input will return the input.
        Default is 'ignore'.

    Returns
    -------
    PasteResult
        An object containing the parsed DataFrame if successful, or None if unsuccessful.
    """
    component_value = _component_func(
        label=label,
        text_color=text_color,
        background_color=background_color,
        hover_background_color=hover_background_color,
        key=key
    )

    if component_value is None:
        return PasteResult()
    elif component_value.startswith('error'):
        if errors == 'raise':
            st.error(f"**Error**: {component_value[7:]}", icon='🚨')
        return PasteResult()

    try:
        df = _csv_to_dataframe(component_value, separator)
        return PasteResult(dataframe=df)
    except Exception as e:
        if errors == 'raise':
            st.error(f"**Error**: Failed to parse data: {str(e)}", icon='🚨')
        return PasteResult()