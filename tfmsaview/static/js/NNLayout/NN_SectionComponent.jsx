import React from 'react'
import NN_InfoListComponent from './../NNConfiguration/NN_InfoListComponent'
import NN_BasicInfoComponent from './../NNConfiguration/NN_BasicInfoComponent'

export default class NN_SectionComponent extends React.Component {
    constructor(props) {
        super(props);
        this.state = {  
        	            tableData : null,
                     };
        this.addNewNNInfo = this.addNewNNInfo.bind(this);
    }

    addNewNNInfo(){
            this.setState({NN_InfoList: <NN_BasicInfoComponent/>});   
    }

    render() {
        return (   
					<main>
					       {this.props.NN_InfoList}
					</main>
        )
    }
}
