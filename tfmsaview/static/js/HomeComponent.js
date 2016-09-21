import React from 'react'
import Api from './utils/Api'
import ReportRepository from './repositories/ReportRepository'

export default class HomeComponent extends React.Component {
    constructor(props) {
        super(props);
    }

   callRestApi() {
        if (true) {
            let params = {
                nn_id: "nn0000005",
                category:"test"
            };
            this.props.reportRepository.getConfigs(params).then((data) => {
                this.setState({data: data})
            });
        }
        else {
            this.props.reportRepository.postServices(`param`).then((data) => {
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
                <div>
                 {this.callRestApi()}
                </div>
            </div>
        )
    }
}

HomeComponent.defaultProps = {
    reportRepository: new ReportRepository(new Api())
};