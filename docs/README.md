# API Documentation For Trivia




`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

---

`GET '/questions?page=${page_number}'`

- Fetches a paginated set of questions, a total number of questions, all categories and current category string.
- Request Arguments: `page` - integer, if doesn't include the `page` parameter, will default to one.
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string

```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 2
    }
  ],
  "totalQuestions": 100,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": "History"
}
```

---

`GET '/categories/${id}/questions'`

- Fetches questions for a cateogry specified by id request argument
- Request Arguments: `id` - integer
- Returns: An object with questions for the specified category, total questions, and current category string

```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 4
    }
  ],
  "totalQuestions": 100,
  "currentCategory": "History"
}
```

---

`DELETE '/questions/${id}'`

- Deletes a specified question using the id of the question
- Request Arguments: `id` - integer
- Returns: Does not need to return anything besides the appropriate HTTP status code. Optionally can return the id of the question. If you are able to modify the frontend, you can have it remove the question using the id instead of refetching the questions.

---

`POST '/quizzes'`

- Sends a post request in order to get the next question
- Request Body:

```json
{
    "previous_questions": [1, 4, 20, 15],
    "quiz_category": {"type": "click", "id": 0}
 }
```
If don't want to filter by category, need to pass as `id`: `0` . It will return the random questions to answer. If `quiz_category` is passed only questions form that selected category will show without duplicate with previous question.

- Returns: a single new question object

```json
{
  "question": {
    "id": 1,
    "question": "This is a question",
    "answer": "This is an answer",
    "difficulty": 5,
    "category": 4
  }
}
```

---

`POST '/questions'`

- Sends a post request in order to add a new question
- Request Body:

```json
{
  "question": "Heres a new question string",
  "answer": "Heres a new answer string",
  "difficulty": 1,
  "category": 3
}
```

- Returns: 
Created Id and all status.
```
{
  "createdQuestionId": 27, 
  "message": "Succesfully created question", 
  "success": true
}

```
---

`POST '/questions'`

- Sends a post request in order to search for a specific question by search term
- Request Body:

```json
{
  "searchTerm": "this is the term the user is looking for"
}
```

- Returns: any array of questions, a number of totalQuestions that met the search term and the current category string

```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 5
    }
  ],
  "totalQuestions": 100,
  "currentCategory": "Entertainment"
}
```

## SAMPLE CURL REQUEST 🕵️‍♀️
> --------------- CURL QUERIES TO TEST ENDPOINTS -------------

```bash
curl -X GET http://127.0.0.1:5000/categories'
````

```bash
curl -X GET http://127.0.0.1:5000/questions?page=1
````

```bash
curl -X DELETE http://127.0.0.1:5000/questions/8 
````

```bash
curl -X POST -H "Content-Type: application/json" -d '{"question":"MilkMocha Country of origin", "answer":"Indonesia", "category":"5", "difficulty":"2"}' http://127.0.0.1:5000/questions 
````

```bash
curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "peanut butter"}' http://127.0.0.1:5000/questions 
````

```bash
curl -X GET http://127.0.0.1:5000/categories/1/questions 
````

```bash
curl -X POST -H "Content-Type: application/json" -d '{"previous_questions": [2, 4], "quiz_category": {"id": 1, "type":"Science"} }' http://127.0.0.1:5000/quizzes 
````

