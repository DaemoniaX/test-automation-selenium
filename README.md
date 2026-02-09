# test-automation-selenium
Automation of tests using selenium python pytest for my react portfolio.

## 🛠 Stack

* **Langage :** Python 3.x
* **Framework :** [Pytest](https://docs.pytest.org/) (Fixtures).
* **Automation :** [Selenium WebDriver](https://www.selenium.dev/).
* **Driver Manager :** `webdriver-manager` (ChromeDriver).

## Covered Scenarios 

The tests cover :

1.  **home Test :** Homepage, navbar, title
2.  **Navigation (Routing) :** (`/CV`, `/graphs`, `/kiduland`...) `pytest.parametrize`.
3.  **search Input :**
    * positive case
    * empty case
4.  **Favorite system :**
    * Add to favorite
    * check
    * delete action
5.  **Swiper :**
    * Carrousel ZuulBad(swiper)
    * Navigation between the slides
6.  **External link :**
    * JSCalculator is being opened


## Installation

### 1. Requirements
* Python 
* Google Chrome 

### 2. Dependencies
In the CMD inside of the project folder :

```bash
pip install selenium pytest webdriver-manager
