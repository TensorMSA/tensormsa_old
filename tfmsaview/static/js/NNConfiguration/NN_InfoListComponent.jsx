import React from 'react';
import PersonalDataTableComponent from './../tables/PersonalDataTableComponent'
import ReportRepository from './../repositories/ReportRepository'
import Api from './../utils/Api'
import NN_InfoListTableComponent from './../tables/NN_InfoListTableComponent'

export default class NN_InfoListComponent extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            tableData : null,
            NN_TableData : null
        }
    }

    getJson(params){
           this.props.reportRepository.getJsonTestData(params).then((tableData) => {
                this.setState({tableData: tableData})
            });
    }


    getCommonNNInfo(params){
           this.props.reportRepository.getCommonNNInfo(params).then((tableData) => {
                this.setState({NN_TableData: tableData})
            });
    }

    NNButtonText(i) {
        switch (i) {
            case 0:
                return "add New";
            case 1:
                return "Delete";
            case 2:
                return "Modify";
            case 3:
                return "Detail";
            default:
                return "";
        }
    }
    NNClickEvent(i){
        switch (i) {
            case 0:
                this.props.addNewNNInfo(); //call parent function to render
            case 1:
                return "";
            case 2:
                return "";
            case 3:
                return "";
            default:
                return "";
        }
    }

    render() {
        return (
            <section>
                <h1 className="hidden">tensor MSA main table</h1>
                    <div className="searchArea">
                        <label className="bullet" for="Name">Name</label>
                        <input type="text" name="Name" placeholder="Name" />
                        <label className="bullet" for="Name2">Name2</label>
                        <input type="text" name="Name2" placeholder="Name" />
                        <button className="btn-sm" type="button" onClick={() => this.getJson()}>search</button>
                        <button className="btn-sm" type="button" onClick={() => this.getCommonNNInfo()}>search</button>
                    </div>
                <div className="container paddingT10">
                    <div className="tblBtnArea">
                        <button type="button" onClick={() => this.NNClickEvent(0)}>
                            {this.NNButtonText(0)}
                        </button>
                        <button type="button" onClick={this.NNClickEvent(1)}>
                            {this.NNButtonText(1)}
                        </button>
                        <button type="button" onClick={this.NNClickEvent(2)}>
                            {this.NNButtonText(2)}
                        </button>
                        <button type="button" onClick={this.NNClickEvent(3)}>
                            {this.NNButtonText(3)}
                        </button>
                    </div>
                    <article>
                        <PersonalDataTableComponent tableData={this.state.tableData} />
                    </article>
                    <article>
                        <NN_InfoListTableComponent NN_TableData={this.state.NN_TableData} />
                    </article>
                </div>
            </section>
        )
    }
}

NN_InfoListComponent.defaultProps = {
    reportRepository: new ReportRepository(new Api())
};