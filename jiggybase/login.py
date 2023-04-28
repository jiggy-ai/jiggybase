
import webbrowser

def is_notebook() -> bool:
    """
    Returns True if code is executed in a notebook (Jupyter, Colab, QTconsole), False otherwise.
    https://stackoverflow.com/a/39662359
    """
    try:
        shell_class = get_ipython().__class__
        for parent_class in shell_class.__mro__:
            if parent_class.__name__ == "ZMQInteractiveShell":
                return True  # Jupyter notebook, Google colab or qtconsole
        return False
    except NameError:
        return False  # Probably standard Python interpreter

    
def window_open(url):    
    print(f"You can find your API Key here: {url}")
    if not is_notebook():
        print("(Attempting to open browser window...)")            
        webbrowser.open(url)
    else:
        pass
        # The following code seems to work to open a web page from a notebook,
        # but when successful it takes the user away to this page somewhat unexpectedly
        # so we will instead rely on the user clicking the above url so they
        # understand what is happening.
        #from IPython.display import Javascript        
        #display(Javascript('window.open("{url}");'.format(url=url)))
