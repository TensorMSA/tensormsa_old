import React from 'react'
import Api from './utils/Api'
import ReportRepository from './repositories/ReportRepository'

export default class HomeComponent extends React.Component {
    constructor(props) {
        super(props);
        this.state = {data : null};
    }

    test_nn_cnn_config_insert_conf(){

    }
    test_nn_cnn_data_post(){

    }
    test_nn_cnn_service_train(){

    }
    test_nn_cnn_service_predict(){

    }

    test_nn_cnn_config_search_conf() {
        let params = {
               nn_id: "nn0000006",
               category:"",
               name : "",
               type : "",
               acc : "",
               train : "",
               config : "",
               table : "",
               query : "",
               datadesc : "",
               datasets : "",
               dir : "default"
           };
           this.checkApiData(params);
            this.props.reportRepository.postConfigNnCnn(params).then((data) => {
                this.setState({data: data})
            });
    }

    checkApiData(params){

    }

    render() {
        return (
            <div className="content">
                <div className="reports">
                    Hello TensorMSA
                </div>
                <div className="getAPI" onClick={() => this.test_nn_cnn_config_search_conf()}>
                 Get API
                </div>
                <div className="displayAPI">
                    {this.state.data}
                </div>
            </div>
        )
    }WW
}

HomeComponent.defaultProps = {
    reportRepository: new ReportRepository(new Api())
};