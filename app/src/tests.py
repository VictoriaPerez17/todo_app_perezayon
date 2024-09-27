from main import validate_password

def test_validate_password():
    # Positive
    success_1 = validate_password("PasswordValid123")
    assert success_1 == True  
    
    success_2 = validate_password("Abcdefg1234")
    assert success_2 == True


    # Negative
    success_3 = validate_password("a")
    assert success_3 == False 

    success_4 = validate_password("sinmayusculas123")
    assert success_4 == False