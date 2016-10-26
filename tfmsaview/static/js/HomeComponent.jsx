import React from 'react'
import NN_HeaderComponent from './NNLayout/NN_HeaderComponent'
import NN_SectionComponent from './NNLayout/NN_SectionComponent'
import NN_FooterComponent from './NNLayout/NN_FooterComponent'
import NN_InfoListComponent from './NNConfiguration/NN_InfoListComponent'
import NN_BasicInfoComponent from './NNConfiguration/NN_BasicInfoComponent'

export default class HomeComponent extends React.Component {
    constructor(props) {
        super(props);
        this.state = {  
                        NN_InfoList : null
                     };
        this.addNewNNInfo = this.addNewNNInfo.bind(this); //need method to send child
        this.getNetInfo = this.getNetInfo.bind(this);
    }

    componentWillMount(){
        this.setState({NN_InfoList: <NN_InfoListComponent addNewNNInfo={this.addNewNNInfo}/>});        
    }

    getNetInfo(){
        this.setState({NN_InfoList: <NN_InfoListComponent addNewNNInfo={this.addNewNNInfo}/>});        
    }

    addNewNNInfo(){
            this.setState({NN_InfoList: <NN_BasicInfoComponent/>});   
    }

    render() {
        return (
            <div>
				<NN_HeaderComponent addNewNNInfo={this.addNewNNInfo} getNetInfo={this.getNetInfo} /> 
				<NN_SectionComponent NN_InfoList={this.state.NN_InfoList}/>
				<NN_FooterComponent/>
			</div>
        )
    }
}
