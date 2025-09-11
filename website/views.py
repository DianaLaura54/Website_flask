from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  
            db.session.add(new_note) 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

@views.route('/automated', methods=['GET', 'POST'])
@login_required
def automated_library():
    """Real Selenium automation of your library"""
    
    if request.method == 'POST':
        action = request.form.get('action')
        
     
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        try:
          
            TEST_EMAIL = "admin2@yahoo.com"
            TEST_PASSWORD = "admin123"
       
            driver.get('http://localhost:5000/login')
            time.sleep(2)
            
      
            email_field = driver.find_element(By.NAME, 'email')
            password_field = driver.find_element(By.NAME, 'password')
            
            email_field.send_keys(TEST_EMAIL)
            password_field.send_keys(TEST_PASSWORD)
            
           
            login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            login_button.click()
            time.sleep(3)
            
         
            if "login" in driver.current_url.lower():
                flash("Selenium login failed! Check your test credentials.", 'error')
                return render_template('automated.html', user=current_user)
            
            if action == 'auto_browse_books':
                
                driver.get('http://localhost:5000/book_list')
                time.sleep(2)
                
                books_found = []
                try:
                   
                    book_rows = driver.find_elements(By.CSS_SELECTOR, 'table tr')[1:] 
                    
                    for row in book_rows[:5]:  
                        cells = row.find_elements(By.TAG_NAME, 'td')
                        if len(cells) >= 4:
                            books_found.append({
                                'name': cells[0].text,
                                'author': cells[1].text,
                                'genre': cells[2].text,
                                'status': cells[3].text
                            })
                except Exception as e:
                    books_found = [{'error': f'Could not parse HTML: {str(e)}'}]
                
                flash(f'Selenium browsed and found {len(books_found)} books!', 'success')
                return render_template('automated.html', user=current_user, books_found=books_found)
            
            elif action == 'auto_search':
                search_term = request.form.get('search_term', 'fiction')
                
             
                driver.get(f'http://localhost:5000/book_list?genre={search_term}')
                time.sleep(2)
                
                try:
                  
                    available_elements = driver.find_elements(By.XPATH, "//td[contains(text(), 'Available')]")
                    total_rows = len(driver.find_elements(By.CSS_SELECTOR, 'table tr')) - 1 
                    
                    flash(f'Selenium searched for "{search_term}" and found {total_rows} books, {len(available_elements)} available!', 'success')
                except Exception as e:
                    flash(f'Selenium search error: {str(e)}', 'error')
            
            elif action == 'auto_reserve':
                driver.get('http://localhost:5000/book_list')
                
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "table"))
                    )
                    
          
                    rows = driver.find_elements(By.CSS_SELECTOR, 'table tr')[1:] 
                    available_books = []
                    for i, row in enumerate(rows):
                        try:
                            cells = row.find_elements(By.TAG_NAME, 'td')
                            if len(cells) >= 6: 
                                book_name = cells[1].text.strip()    
                                status_text = cells[4].text.strip()         
                                if status_text == 'Available':
                                    try:
                                        reserve_button = row.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
                                        if reserve_button.is_displayed() and reserve_button.is_enabled():
                                            hidden_input = row.find_element(By.NAME, 'reserve')
                                            book_id_from_input = hidden_input.get_attribute('value')
                                            
                                            available_books.append({
                                                'button': reserve_button,
                                                'book_id': book_id_from_input,
                                                'book_name': book_name,
                                                'row_index': i
                                            })
                                    except:
                                        continue 
                                
                        except Exception as e:
                            continue  

                    if available_books:
                       
                        import random
                        chosen_book = random.choice(available_books)
                    
                        try:
                            driver.execute_script("arguments[0].scrollIntoView(true);", chosen_book['button'])
                            time.sleep(1)
                            chosen_book['button'].click()
                            time.sleep(2)
                            
                            flash(f'Selenium randomly reserved "{chosen_book["book_name"]}" (ID: {chosen_book["book_id"]})!', 'success')
                            
                        except Exception as click_error:
                            flash(f'Found available book but could not click: {str(click_error)}', 'error')
                    else:
                        flash('No books with "Available" status found on the page', 'error')
                        
                except Exception as e:
                    flash(f'Selenium reserve error: {str(e)}', 'error')
            
            elif action == 'auto_donate':
               
                driver.get('http://localhost:5000/donate')
                time.sleep(2)
                
                try:
                    name_field = driver.find_element(By.NAME, 'name')
                    author_field = driver.find_element(By.NAME, 'author')
                    location_field = driver.find_element(By.NAME, 'location')
                    genre_field = driver.find_element(By.NAME, 'genre')
                    
                 
                    import random
                    book_titles = ['Selenium Guide', 'Web Automation', 'Python Testing', 'Browser Control']
                    authors = ['Auto Author', 'Test Writer', 'Selenium Master']
                    locations = ['Gheorgheni', 'Zoriilor', 'Marasti', 'Manastur']

                    book_title = random.choice(book_titles)
                    author_name = random.choice(authors)
                    location_name = random.choice(locations)
                    
                    name_field.send_keys(book_title)
                    author_field.send_keys(author_name)
                    location_field.send_keys(location_name)
                    genre_field.send_keys('Technology')
                    
                   
                    submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
                    submit_button.click()
                    time.sleep(2)
                    
                    
                    page_text = driver.page_source
                    if "Thank you" in page_text or "added" in page_text.lower():
                        flash(f'Selenium donated "{book_title}" by {author_name}!', 'success')
                    else:
                        flash('Selenium submitted donation form but no success message found', 'warning')
                        
                except Exception as e:
                    flash(f'Selenium donation error: {str(e)}', 'error')
                    
        except Exception as e:
            flash(f'Selenium automation error: {str(e)}', 'error')
        finally:
            driver.quit()
    
    return render_template('automated.html', user=current_user)