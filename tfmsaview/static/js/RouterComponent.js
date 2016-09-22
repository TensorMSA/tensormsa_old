import React from 'react'
import { Router, Route, Link } from 'react-router'
import HomeComponent from './HomeComponent'

export default class RouterComponent extends React.Component {
    render() {
        return (   
            <div>
                <Router>
                    <Route path="/" component={HomeComponent} />
                </Router>
            </div>
        )
    }
}