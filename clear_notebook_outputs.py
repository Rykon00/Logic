import os
import nbformat

from nbformat import NotebookNode


def strip_outputs(notebook_path: str) -> None:
    """
    Öffnet ein Jupyter-Notebook, entfernt alle Ausgaben und
    setzt execution_count auf None, und speichert es inplace.
    Überspringt Dateien, die keine gültigen JSON-Notebooks sind.
    """
    try:
        nb = nbformat.read(notebook_path, as_version=nbformat.NO_CONVERT)
    except Exception as e:
        # z.B. NotJSONError oder andere Lesefehler
        print(f"⚠️ Skipping non-JSON notebook: {notebook_path} ({e.__class__.__name__})")
        return

    """
    Öffnet ein Jupyter-Notebook, entfernt alle Ausgaben und
    setzt execution_count auf None, und speichert es inplace.
    """
    nb = nbformat.read(notebook_path, as_version=nbformat.NO_CONVERT)
    modified = False
    for cell in nb.cells:
        if cell.cell_type == 'code':
            if cell.get('outputs'):
                cell['outputs'] = []
                modified = True
            if cell.get('execution_count') is not None:
                cell['execution_count'] = None
                modified = True
    if modified:
        nbformat.write(nb, notebook_path)
        print(f"🧹 Cleared outputs in: {notebook_path}")


def main(root_dir: str = '.') -> None:
    """
    Durchläuft rekursiv alle .ipynb Dateien unter root_dir
    und ruft strip_outputs auf.
    """
    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            if fname.endswith('.ipynb'):
                path = os.path.join(dirpath, fname)
                strip_outputs(path)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='Clear outputs from all Jupyter notebooks in a directory.')
    parser.add_argument(
        'path', nargs='?', default='.',
        help='Root directory to scan for notebooks')
    args = parser.parse_args()
    main(args.path)
    print("✅ All notebook outputs cleared.")
