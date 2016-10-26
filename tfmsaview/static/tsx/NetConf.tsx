import * as React from 'react'
import {render} from 'react-dom'
import Header from './header'
import Section from './section'
import Footer from './footer'
import '../scss/style.scss';

class NetConf extends React.Component<any, any> {
    render() {
        return (
            <div>
                <Header/>
                <Section/>
                <Footer/>
            </div>
            
        ) 
    }
}

render(<NetConf/>, document.getElementById('main'));