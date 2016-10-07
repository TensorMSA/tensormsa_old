import React from 'react'
import Api from './utils/Api'
import ReportRepository from './repositories/ReportRepository'
import PersonalDataTableComponent from './tables/PersonalDataTableComponent'

export default class HomeComponent extends React.Component {
    constructor(props) {
        super(props);
        this.state = {  data : null, 
                        tableData : null
                     };
    }

    case1(){
        let params = {
               nn_info : { nn_id: "nn0000009",
                           category:"test",
                           name : "test",
                           type : "cnn",
                           acc : "",
                           train : "",
                           config : "Y",
                           table : "TEST2",
                           query : "select * from TEST1",
                           datadesc:"{'name':'none', 'univ':'rank', 'org' : 'cate' , 'eng' : 'cont', 'grade' : 'tag', 'gender' :'cate' , 'age' : 'cont'}",
                           datasets:"",
                           dir : "default"},
               nn_conf : {
                            data:
                                {
                                    datalen: 96,
                                    taglen: 2,
                                    matrix: [12, 8],
                                    learnrate: 0.01,
                                    epoch:10
                                },
                            layer:
                                [
                                    {
                                        type: "input",
                                        active: "relu",
                                        cnnfilter: [2, 2],
                                        cnnstride: [1, 1],
                                        maxpoolmatrix: [2, 2],
                                        maxpoolstride: [1, 1],
                                        node_in_out: [1, 16],
                                        regualizer: "",
                                        padding: "SAME",
                                        droprate: ""
                                    },
                                    {
                                        type: "out",
                                        active: "softmax",
                                        cnnfilter: "",
                                        cnnstride: "",
                                        maxpoolmatrix: "",
                                        maxpoolstride: "",
                                        node_in_out: [64, 2],
                                        regualizer: "",
                                        padding: "SAME",
                                        droprate: ""
                                    }
                                ]
                        }
           };
           this.props.reportRepository.postConfigNnCnn(params).then((data) => {
                this.setState({data: data})
            });

    }
    case2(){
        let params = "nn0000009"
               this.props.reportRepository.getConfigNnCnn(params).then((data) => {
                    this.setState({data: data})
                });

    }
    case3(){
        let params = {
                    nn_id: "nn0000009",
                    table: "TEST2",
                    data:[{'name':'Andy', 'univ':'SKKU', 'org' : '1', 'eng' : '800' , 'grade' : 'A', 'gender' : 'female', 'age' : '50'},
                            {'name':'Kim', 'univ':'SKKU', 'org' : '2', 'eng' : '800' , 'grade' : 'A', 'gender' : 'female', 'age' : '35'},
                            {'name':'Kim', 'univ':'SKKU', 'org' : '3', 'eng' : '800' , 'grade' : 'A', 'gender' : 'male', 'age' : '65'},
                            {'name':'Kim', 'univ':'SKKU', 'org' : '4', 'eng' : '800' , 'grade' : 'A', 'gender' : 'female', 'age' : '70'},
                            {'name':'Kim', 'univ':'SKKU', 'org' : '5', 'eng' : '800' , 'grade' : 'A', 'gender' : 'male', 'age' : '25'},
                            {'name':'Kim', 'univ':'SKKU', 'org' : '5', 'eng' : '800' , 'grade' : 'A', 'gender' : 'male', 'age' : '25'},
                            {'name':'Kim', 'univ':'SKKU', 'org' : '5', 'eng' : '800' , 'grade' : 'A', 'gender' : 'male', 'age' : '25'},
                            {'name':'Kim', 'univ':'e', 'org' : '5', 'eng' : '800' , 'grade' : 'B', 'gender' : 'male', 'age' : '25'},
                            {'name':'Kim', 'univ':'d', 'org' : '4', 'eng' : '800' , 'grade' : 'B', 'gender' : 'female', 'age' : '70'},
                            {'name':'Kim', 'univ':'e', 'org' : '5', 'eng' : '800' , 'grade' : 'B', 'gender' : 'male', 'age' : '25'},
                            {'name':'Kim', 'univ':'e', 'org' : '5', 'eng' : '800' , 'grade' : 'B', 'gender' : 'male', 'age' : '25'},
                            {'name':'Kim', 'univ':'e', 'org' : '5', 'eng' : '800' , 'grade' : 'B', 'gender' : 'male', 'age' : '25'},
                            {'name':'Kim', 'univ':'e', 'org' : '5', 'eng' : '800' , 'grade' : 'B', 'gender' : 'male', 'age' : '25'},
                            {'name':'Kim', 'univ':'d', 'org' : '4', 'eng' : '800' , 'grade' : 'B', 'gender' : 'female', 'age' : '70'},
                            {'name':'Kim', 'univ':'e', 'org' : '5', 'eng' : '800' , 'grade' : 'B', 'gender' : 'male', 'age' : '25'},
                            {'name':'Kim', 'univ':'e', 'org' : '5', 'eng' : '800' , 'grade' : 'B', 'gender' : 'male', 'age' : '25'},
                            {'name':'Kim', 'univ':'e', 'org' : '5', 'eng' : '800' , 'grade' : 'B', 'gender' : 'male', 'age' : '25'},
                            {'name':'Kim', 'univ':'e', 'org' : '5', 'eng' : '800' , 'grade' : 'B', 'gender' : 'male', 'age' : '25'},
                            {'name':'Kim', 'univ':'d', 'org' : '4', 'eng' : '800' , 'grade' : 'B', 'gender' : 'female', 'age' : '70'}],
                    query: ""
               };
               this.props.reportRepository.postDataNnCnn(params).then((data) => {
                    this.setState({data: data})
                });

    }

    case4(){
        let params = "TEST2"
                   this.props.reportRepository.getDataNnCnn(params).then((data) => {
                        this.setState({data: data})
                    });
    }

    case5(){
        let params = {
                    nn_id: "nn0000009",
                    table: "TEST2",
                    data:[{'name':'Andy', 'univ':'SKKU', 'org' : '1', 'eng' : '800' , 'grade' : 'A', 'gender' : 'female', 'age' : '50'},
                            {'name':'Kim', 'univ':'SKKU', 'org' : '2', 'eng' : '800' , 'grade' : 'A', 'gender' : 'female', 'age' : '35'},
                            {'name':'Kim', 'univ':'SKKU', 'org' : '3', 'eng' : '800' , 'grade' : 'A', 'gender' : 'male', 'age' : '65'},
                            {'name':'Kim', 'univ':'SKKU', 'org' : '4', 'eng' : '800' , 'grade' : 'A', 'gender' : 'female', 'age' : '70'},
                            {'name':'Kim', 'univ':'SKKU', 'org' : '5', 'eng' : '800' , 'grade' : 'A', 'gender' : 'male', 'age' : '25'},
                            {'name':'Kim', 'univ':'SKKU', 'org' : '5', 'eng' : '800' , 'grade' : 'A', 'gender' : 'male', 'age' : '25'},
                            {'name':'Kim', 'univ':'SKKU', 'org' : '5', 'eng' : '800' , 'grade' : 'A', 'gender' : 'male', 'age' : '25'},
                            {'name':'Kim', 'univ':'e', 'org' : '5', 'eng' : '800' , 'grade' : 'B', 'gender' : 'male', 'age' : '25'},
                            {'name':'Kim', 'univ':'d', 'org' : '4', 'eng' : '800' , 'grade' : 'B', 'gender' : 'female', 'age' : '70'},
                            {'name':'Kim', 'univ':'e', 'org' : '5', 'eng' : '800' , 'grade' : 'B', 'gender' : 'male', 'age' : '25'},
                            {'name':'Kim', 'univ':'e', 'org' : '5', 'eng' : '800' , 'grade' : 'B', 'gender' : 'male', 'age' : '25'}],
                    query: ""
               };
               this.props.reportRepository.putDataNnCnn(params).then((data) => {
                    this.setState({data: data})
                });
    }


    case6(){
        let params = {
                nn_id: "nn0000009" ,
                nn_type : "cnn",
                run_type : "local",
                epoch : 5,
                testset : 10 ,
                predict_data:""
           };
           this.props.reportRepository.postTrainNnCnn(params).then((data) => {
                this.setState({data: data})
            });
    }

    case7(){
        let params = {
                nn_id: "nn0000009" ,
                nn_type : "cnn",
                run_type : "local",
                epoch : 5,
                testset : 10 ,
                predict_data:[{'name':'Andy', 'univ':'a', 'org' : '1', 'eng' : '800' , 'gender' : 'female', 'age' : '50'}]
           };
           this.props.reportRepository.postPredictNnCnn(params).then((data) => {
                this.setState({data: data})
            });
    }

    getJson(params){
           this.props.reportRepository.getJsonTestData(params).then((tableData) => {
                this.setState({tableData: tableData})
            });
    }

    render() {
        return (
            <div className="content">
                <div className="reports">
                    Hello TensorMSA
                </div>
                <div>
                <button className="getAPI1" onClick={() => this.case1()}> create NN conf </button>
                <button className="getAPI2" onClick={() => this.case2()}> Search NN conf </button>
                <button className="getAPI3" onClick={() => this.case3()}> Create Data Table</button>
                <button className="getAPI4" onClick={() => this.case4()}> Search Data Table</button>
                <button className="getAPI5" onClick={() => this.case5()}> Add Data Table </button>
                <button className="getAPI6" onClick={() => this.case6()}> Start Tarining </button>
                <button className="getAPI7" onClick={() => this.case7()}> Predict Result </button>
                <button className="testJson" onClick={() => this.getJson()}> Test JSON Table</button>
                </div>
                <div className="displayAPI">
                    {this.state.data}
                </div>
                <div className="jsonTestTable">
                    <PersonalDataTableComponent tableData={this.state.tableData} />
                </div>
            </div>
        )
    }
}

HomeComponent.defaultProps = {
    reportRepository: new ReportRepository(new Api())
};