import pytest
from spyctral import read_fisa

# Definición de los casos de prueba parametrizados


@pytest.mark.parametrize("input_file, expected_version, expected_reddening",
                         "expected_NP" [
    ("test_file1.dat", "1.0", 0.5, 0.5),
    ("test_file2.dat", "2.0", 0.7, 0.7),
    ("test_file3.dat", "3.0", 0.3, 0.45),
                                        ])
def test_read_fisa_parametrized(input_file, expected_version,
                                expected_reddening, expected_NP):
    # Crea un archivo de prueba con contenido específico
    tmp_path = 'Draft/fisa_test_files'
    test_file = tmp_path / input_file
    test_file.write_text(
        f" # SPECTRUM ANALYZED WITH FISA v. {expected_version}\n"
        " # Date 10/20/2023; time 12:34:56\n"
        f" # Reddening: {expected_reddening}\n"
        " # Adopted Templated: file_name.dat\n"
        " # Normalization Point: {expected_NP}\n"
        " # Index 0 = Spectrum 1\n"
        " # Index 1 = Spectrum 2\n"
        "400.0 0.1\n"
        "450.0 0.2\n"
    )
    summary = read_fisa(test_file)
    
    assert summary.header["fisa_version"] == expected_version
    assert summary.header["reddening"] == expected_reddening
    assert summary.header['normalization_Point'] == expected_NP
    # Agregar más aserciones según sea necesario

