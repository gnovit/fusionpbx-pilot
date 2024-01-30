Feature: Login
    Simple login on FusionPBX.

    Scenario: Login with invalid user
    Given Invalid user
        | name | password |
        | foo  | bar      |

    When Open Login Page
    Then Returns invalid login error.

    Scenario: Login with valid user
    Given Valid User
        | name  | password         |
        | admin | c0mpl3x_password |
    
    When any page was opened
    Then login

    Scenario: Access a page with a valid user, but no permission.
    Given Valid user, but no permission
        | name   | password         |
        | admin1 | c0mpl3x_password |

    When a restricted page was opened
    Then return no permission.