import React from 'react';
import NN_InfoListTableRowComponent from './NN_InfoListTableRowComponent';

export default class NN_InfoListTableComponent extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        //check null for initialize dom
        if (!this.props.NN_TableData) {return null;}

        return (
            <div className="table">
                <table>
                    <thead>
                    <tr>
                        <th>category</th>
                        <th>subcate</th>
                        <th>desc</th>
                        <th>name</th>
                        <th>created</th>
                    </tr>
                    </thead>
                    <tbody>
                    {<NN_InfoListTableRowComponent NN_TableData={this.props.NN_TableData}/>}
                    </tbody>
                </table>
            </div>
        )
    }
}