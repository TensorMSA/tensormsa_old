import * as React from 'react'

export default class Section extends React.Component<any,any> {
    render() {
        return (
            <section>                    
                <div>
                    <div className='column features'>
                        <h4>Features</h4>
                    </div>
                    <div className='column hidden-layers'>
                        <h4>Hidden</h4>
                    </div>
                    <div className='column output'>
                        <h4>Output</h4>
                    </div>
                </div>                
            </section>
        )
    }
}