import React from 'react';
import FileUpload from 'react-fileupload';
import DropzoneComponent from 'react-dropzone-component';
import Api from './../../utils/Api'
import ReportRepository from './../../repositories/ReportRepository'

export default class NN_PredictResultComponent extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            result:'cifar 결과',
            NN_TableData: null,
            selModalView: null,
            NN_ID : '',
            networkList: null,
            networkTitle: '',
            dropzoneConfig: {
            //    iconFiletypes: ['.jpg', '.png', '.gif'],
                showFiletypeIcon: true,
                postUrl: 'no-url'            
            }
        };
    }

    componentDidMount(){
        console.log("CIFA did mounted!!!!")
        this.getNetworkList();
        console.log('NN_ID : ' + this.context.NN_ID)   
    }    

    updateResult(result) {
        console.log('updateResult Called : ' + result);
        this.setState({result: JSON.parse(result).result});
    }

    setDropzone(dropzone) {
        console.log('setDropzone')
        console.log(dropzone)
        this.dropzone = dropzone
    }

    removeDropZoneFile() {
        if (this.dropzone.files.length > 1) {
            this.dropzone.removeFile(this.dropzone.files[0]);
        }
    }

    getNetworkList(){
        //let request
        this.props.reportRepository.getCommonNNInfo().then((network_list) => {
            let optionRows = [];
            let networkData = {};
            console.log(network_list)
            for (var i in network_list) {
                let networkId = network_list[i]['pk']
                optionRows.push(<option key={i} value={networkId}>{networkId}</option>)
                networkData[networkId] = network_list[i]
            }
            this.setState({networkList : optionRows})
            this.setState({NN_TableData: networkData})
            console.log('optionRows')
            console.log(optionRows)
            this.setNetwork(optionRows[0].props.value)
        });
    }

    onNetworkChanged(e) {
        this.setNetwork(e.target.value)
    }

    setNetwork(networkId)
    {
        console.log('value : ' +  networkId)
        console.log(this.state.NN_TableData[networkId]['fields'])
        this.setState({NN_ID: networkId})
        this.setState({networkTitle: this.state.NN_TableData[networkId]['fields']['name']});
        this.setDropZoneUrl(networkId)
    } 

    setDropZoneUrl(networkId) {
        this.setState({dropzoneConfig: {
                iconFiletypes: ['.jpg', '.png', '.gif'],
                showFiletypeIcon: true,
                postUrl: 'http://52.78.19.96:8989/api/v1/type/cifar/kind/ten/'             
            }})     
    }   

    render() {
        var djsConfig = { 
            addRemoveLinks: false,
            acceptedFiles: "image/jpeg,image/png,image/gif",
            dictDefaultMessage: '파일 여기'
         }
        var eventHandlers = { 
            init: (passedDropzone) => {
                this.setDropzone(passedDropzone)
            },
            success: (e, response) => {
                console.log(response);
                this.updateResult(response);
            },
            processing: (file) => {
                console.log('processing : ' )
                console.log(file);
            },
            addedfile: (file) => {
                console.log('addedfile : ')
                console.log(file)
                console.log(this.dropzone)
                this.removeDropZoneFile();
            }
            

            

        }


        

        return (
            <div className="container tabBody">
            <article>
                <table className="form-table">
                    <colgroup>
                    <col width="20%" />
                    <col width="30%" />
                    <col width="20%" />
                    </colgroup>
                    <thead>
                        <tr>
                            <th>Network ID</th>
                            <td className="left">
                                <select onChange={this.onNetworkChanged.bind(this)} value={this.state.NN_ID}>
                                    {this.state.networkList}  
                                </select>
                            </td>
                            <th>제목</th>
                            <td className="left">{this.state.networkTitle}</td>
                        </tr>
                    </thead>
                </table>
                
                <div className="predict-box-wrap">
                    <div className="predict-box-container">
                        <div className="predict-tit">
                            <h1 className="circle-blue">Drag&#38;Drop</h1>
                        </div>
                        <div className="predict-tit">
                            <h1 className="circle-blue">Result</h1>
                        </div>
                        
                        <div className="predict-box-body">
                            <section className="drag-section">
                                <div className="drag-img">
                                     <DropzoneComponent config={this.state.dropzoneConfig}
                                        eventHandlers={eventHandlers}
                                        djsConfig={djsConfig} 
                                        />
                                </div>
                            </section>
                            <section className="result-section">
                                <div className="result-value">{this.state.result}</div>
                            </section>
                        </div>
                    </div>
                </div>
            </article>
                                      
            </div>  

/*
            <section>
                <h1 className="hidden">PredictResult</h1>
                <ul className="tabHeader">
                  
                    <div className="btnArea">
                        <button type="button" className="img-btn save">Select file</button>
                        <button type="button" className="img-btn save">Predict</button>   
                        
                          
                    </div>
                </ul>
                <FileUpload options={options} updateState={this.updateResult.bind(this)}>
                    <button ref="chooseBtn">choose</button>
                    <button ref="uploadBtn">upload</button>
                   
                </FileUpload>
                 <div className="container tabBody">
                    <article>
                    <button ref="uploadBtn" onClick={this.dropzoneUpload.bind(this)} >upload</button>
                    <DropzoneComponent config={componentConfig}
                       eventHandlers={eventHandlers}
                       djsConfig={djsConfig} 
                        updateState={this.updateResult.bind(this)}
                       />,

                       
                        <dl className="data-box clearB w100p hInherit marginT10">
                            <dt><span className="circle-green">Sample Data</span></dt>
                            <dd>
                              <div>result : {this.state.result}</div>  
                            </dd>
                        </dl>
                    </article>
                 </div>  
            </section>
*/
        )
    }
}



NN_PredictResultComponent.defaultProps = {
    reportRepository: new ReportRepository(new Api())
}; 


