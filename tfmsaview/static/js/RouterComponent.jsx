import React from 'react'
import { Router, Route, Link, browserHistory } from 'react-router'
import HomeComponent from './HomeComponent'

export default class RouterComponent extends React.Component {
    render() {
        return (   
                <Router history = {browserHistory}>
                    <Route path="/" component={HomeComponent} />
                </Router>
        )
    }
}