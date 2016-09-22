import React from 'react'
import Api from './utils/Api'
import ReportRepository from './repositories/ReportRepository'

export default class HomeComponent extends React.Component {
    constructor(props) {
        super(props);
        this.state = {data : null}
        this.callRestApi = this.callRestApi.bind(this);
    }

   callRestApi() {
        this.setState({data: null});
        let req_data = [ 0 , 0 , 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,
                   0 , 0 , 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,
                   0 , 0 , 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,
                   0 , 0 , 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,
                   0 , 0 , 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,
                   0 , 0 , 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,
                   0 , 0 , 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,
                   0 , 0 , 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ];

        if (true) {
          /*  let params = {
                nn_id: "nn0000005" ,
                nn_type : "cnn",
                run_type : "local",
                 epoch : "",
                 testset : "" ,
                 predict_data:req_data
            };


            this.props.reportRepository.postServices(params).then((data) => {
                this.setState({data: data})
            });
                */

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

            this.props.reportRepository.postConfigs(params).then((data) => {
                this.setState({data: data})
            });


        }
        else {
            this.props.reportRepository.postServices('param').then((data) => {
                this.setState({data: data});
            });
        }
    }

    render() {
        return (
            <div className="content">
                <div className="reports">
                    Hello TensorMSA
                </div>
                <div className="getAPI" onClick={() => this.callRestApi()}>
                 Get API
                </div>
                <div className="displayAPI">
                    {this.state.data}
                </div>
            </div>
        )
    }
}

HomeComponent.defaultProps = {
    reportRepository: new ReportRepository(new Api())
};