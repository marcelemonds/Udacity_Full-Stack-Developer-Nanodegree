import React, { Component } from 'react';

import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';
import $ from 'jquery';

const  BASE_API_URL = 'http://localhost:5000'

class QuestionView extends Component {
  constructor(){
    super();
    this.state = {
      questions: [],
      page: 1,
      totalQuestions: 0,
      categories: {},
      currentCategory: null,
      resetPage: true, 
      resetPageCount: 0
    }
  }

  componentDidMount() {
    this.getQuestions();
  }

  getQuestions = () => {
    $.ajax({
      url: `${BASE_API_URL}/questions?page=${this.state.page}`,
      type: "GET",
      success: (result) => {
        const questions = result.questions.map(question => {
          result.categories.forEach(category => {
            if(category.id === question.category){
              question.category = category.type;
            }
          });
          return question;
        });
        this.setState({
          questions: questions,
          totalQuestions: result.total_questions,
          categories: result.categories,
          currentCategory: result.current_category,
          resetPage: true,
          resetPageCount: 0})
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  selectPage(num) {
    this.setState({page: num}, () => this.getQuestions());
  }

  createPagination(){
    let pageNumbers = [];
    let maxPage = Math.ceil(this.state.totalQuestions / 10)
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
        <span
          key={i}
          className={`page-num ${i === this.state.page ? 'active' : ''}`}
          onClick={() => {this.selectPage(i)}}>{i}
        </span>)
    }
    return pageNumbers;
  }

  getByCategory= (id) => {
    $.ajax({
      url: `${BASE_API_URL}/categories/${id}/questions`,
      type: "GET",
      success: (result) => {
        const questions = result.questions.map(question => {
          question.category = result.current_category.type;
          return question;
        });
        this.setState({
          questions: questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  submitSearch = (searchTerm) => {
    $.ajax({
      url: `${BASE_API_URL}/questions`, //TODO: update request URL
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({searchTerm: searchTerm}),
      xhrFields: {
        withCredentials: false
      },
      crossDomain: true,
      success: (result) => {
        const questions = result.questions.map(question => {
          this.state.categories.forEach(category => {
            if(category.id === question.category){
              question.category = category.type;
            }
          });
          return question;
        });
        this.setState({
          questions: questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  questionAction = (id) => (action) => {
    if(action === 'DELETE') {
      if(window.confirm('are you sure you want to delete the question?')) {
        $.ajax({
          url: `${BASE_API_URL}/questions/${id}`, //TODO: update request URL
          type: "DELETE",
          success: (result) => {
            if(this.state.currentCategory){
              const { id } = this.state.currentCategory;
              this.getByCategory(id);
            }else{
              this.getQuestions();
            }
          },
          error: (error) => {
            alert('Unable to load questions. Please try your request again')
            return;
          }
        })
      }
    }
  }

  render() {
    return (
      <div className="question-view">
        <div className="categories-list">
          <h2 onClick={() => {this.getQuestions()}}>Categories</h2>
          <ul>
            {Object.keys(this.state.categories).map((id, ) => (
              <li key={id} onClick={() => {this.getByCategory(this.state.categories[id].id)}}>
                {this.state.categories[id].id}
                <img className="category" src={`${this.state.categories[id].type.toLowerCase()}.svg`}/>
              </li>
            ))}
          </ul>
          <Search submitSearch={this.submitSearch}/>
        </div>
        <div className="questions-list">
          <h2>Questions</h2>
          {this.state.questions.map((q, ind) => (
            <Question
              key={q.id}
              question={q.question}
              answer={q.answer}
              category={q.category.toLowerCase()} 
              difficulty={q.difficulty}
              questionAction={this.questionAction(q.id)}
            />
          ))}
          <div className="pagination-menu">
            {this.createPagination()}
          </div>
        </div>

      </div>
    );
  }
}

export default QuestionView;
