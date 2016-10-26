import React from 'react'

export default class NN_InfoListTableRowComponent extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <tr>
                <td>{this.props.NN_TableData.category}</td>
                <td>{this.props.NN_TableData.subcate}</td>
                <td>{this.props.NN_TableData.desc}</td>
                <td>{this.props.NN_TableData.name}</td>
                <td>{this.props.NN_TableData.created}</td>
            </tr>
        )
    }
}