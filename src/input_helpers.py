from enums import FxEditions, PbEditions, PeEditions, SbEditions, NeEditions
from scraper import set_edition

def select_format():
    """
    Indica al usuario que seleccione un formato y devuelve la clase de enumeración correspondiente.

    Returns:
        Enum: La clase de enumeración del formato seleccionado.
    """
    formats = {
        1: ("Primera Era", PeEditions),
        2: ("Primer Bloque", PbEditions),
        3: ("Segundo Bloque", SbEditions),
        4: ("Furia Extendido", FxEditions),
        5: ("Nueva Era (Imperio)", NeEditions)
    }
    
    print("Selecciona un formato:")
    for i, (name, _) in formats.items():
        print(f"{i}. {name}")

    choice = int(input("Ingresa el número del formato deseado: "))
    selected_format = formats[choice][1]
    return selected_format

def select_edition(format_enum):
    """
    Indica al usuario que seleccione una edición de la enumeración de formato dada y establece la edición.
    
    Args:
        format_enum (Enum): La clase enum del formato para seleccionar una edición.

    Returns:
        str: El valor de la edición seleccionada.
    """
    print("Selecciona una edición:")
    for i, edition in enumerate(format_enum, 1):
        print(f"{i}. {edition.name}")

    choice = int(input("Ingresa el número de la edición deseada: "))
    selected_edition = list(format_enum)[choice - 1]
    set_edition(selected_edition.value)
    return selected_edition.value