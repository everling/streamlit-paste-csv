function sendValue(value) {
  Streamlit.setComponentValue(value);
}

async function parseClipboardData() {
  try {
    const text = await navigator.clipboard.readText();
    sendValue(text);
  } catch (error) {
    console.error('Error reading clipboard:', error);
    sendValue("error: " + error);
  }
}

function onRender(event) {
  if (!window.rendered) {
    const {label, text_color, background_color, hover_background_color, key} = event.detail.args;
    const pasteButton = document.getElementById('paste_button');

    pasteButton.innerHTML = label;
    pasteButton.style.color = text_color;
    pasteButton.id = key;

    pasteButton.addEventListener('click', parseClipboardData);

    pasteButton.style.backgroundColor = background_color;

    pasteButton.addEventListener('mouseover', function() {
      pasteButton.style.backgroundColor = hover_background_color;
    });

    pasteButton.addEventListener('mouseout', function() {
      pasteButton.style.backgroundColor = background_color;
    });

    pasteButton.style.fontFamily = event.detail.theme.font;

    window.rendered = true;
  }
}

Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender);
Streamlit.setComponentReady();
Streamlit.setFrameHeight(40);