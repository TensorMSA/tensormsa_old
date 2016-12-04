import React from 'react'
import ReportRepository from './../../repositories/ReportRepository'
import Api from './../../utils/Api'
import SpinnerComponent from './../../NNLayout/common/SpinnerComponent'

export default class MetaStore_TableLayout extends React.Component {
	constructor(props) {
        super(props)
        this.state = {
            selectValue:[],//initail lodaing is meta
            cellfeature:{},
            label:{},
            dataFormatTypes:{},
            dataFormatTypesLabel:{},
            dataFramePost:null,
            selectdataFormatTypes:{},
            celStateHeaderSelectBoxValue:{},
            WdnnTableColumnType:{}
            };
        this.celHeaderSelectBoxValue = {};
        this.celHeaderSelectBoxValue2 = {};
        this.first_time = true;
    }
     componentDidUpdate() {
    //     console.log("componentDidUpdatechild")
    //     if(!this.props.WdnnTableColumnType) {return null;}
    //     this.setState({celStateHeaderSelectBoxValue:this.props.WdnnTableColumnType})
    //     // Use Materialize custom select input
    //     calWdnnTableColumnType()
    //     //this.refs.s1.forceUpdate();
           this.getCategoryType3(this.props.WdnnTableColumnType)
    }
    setWdnnTableColumnType()
    {
            console.log("setWdnnTableColumnType  true")
            this.first_time = true;
    }
    calWdnnTableColumnType()
    {
        console.log("calWdnnTableColumnTypechild")
        if(!this.props.WdnnTableColumnType) {return null;}
        console.log("calWdnnTableColumnTypechild")
        let CalWdnnTableColumnType = {}
        for(let columnValuesType of this.props.WdnnTableColumnType){
            console.log(columnValuesType)
            //add colums

        }

    }
    shouldComponentUpdate(nextProps, nextState){
        console.log("shouldComponentUpdate: " + JSON.stringify(nextProps) + " " + JSON.stringify(nextState));
        return true;
    }
    handleChange(selectedValue){
        //console.log("lookup dictionary")
        //console.log(selectedValue.target)
        //console.log(selectedValue.target.id)
        //console.log(selectedValue.target.value)
        let selectDataFormatType = this.state.dataFormatTypes
        let selectDataFormatLabel = this.state.dataFormatTypesLabel
        let selectCellFeature = this.state.cellfeature
        let selectDataFormatTypeCell = {}
        let selectDataFormatTypeLabel = {}
        //this.celHeaderSelectBoxValue[selectedValue.target.id]=selectedValue.target.value
        let _celHeaderSelectBoxValue = {}
        let _celHeaderSelectBox = {}
        _celHeaderSelectBoxValue["conlumn_type"] = selectedValue.target.value
        _celHeaderSelectBox[selectedValue.target.id] = _celHeaderSelectBoxValue
        this.setState({celStateHeaderSelectBoxValue:_celHeaderSelectBox})

        //CONTINUOUS CATEGORICAL
        if ('CATEGORICAL' == selectedValue.target.value){
            console.log(selectedValue.target.value)
            selectDataFormatTypeCell['column_type'] = selectedValue.target.value
            selectDataFormatType[selectedValue.target.id] = selectDataFormatTypeCell
            this.setState({dataFormatTypes : selectDataFormatType})
        }
        if ('CONTINUOUS' == selectedValue.target.value){
            console.log(selectedValue.target.value)
            selectDataFormatTypeCell['column_type'] = selectedValue.target.value
            selectDataFormatType[selectedValue.target.id] = selectDataFormatTypeCell
            this.setState({dataFormatTypes : selectDataFormatType})
        }
        if ('LABEL' == selectedValue.target.value){
            console.log(selectedValue.target.value)
            selectDataFormatTypeLabel['column_type'] = selectedValue.target.value
            selectDataFormatLabel[selectedValue.target.id] = selectDataFormatTypeLabel
            this.setState({dataFormatTypesLabel : selectDataFormatLabel})
        }
        selectCellFeature['cell_feature'] = selectDataFormatType
        selectCellFeature['label'] = selectDataFormatLabel
        this.setState({cellfeature : selectCellFeature}) 
        this.celHeaderSelectBoxValue2 = selectCellFeature;
    }
    dataFramePost(opt_url){

        //error check assert
        console.log("dataframpost")
        this.props.reportRepository.postWdnnDataFrameFormat(opt_url,this.state.cellfeature).then((tableData) => {
            console.log('dataframepost results')
            this.setState({dataFramePost: tableData['result']})
        });
    }
    checkColumnDataType(){
        // Label이 하나만 있는가?
        // let flag = this.state.cellfeature.map(function(_labelExist){
        //     console.log(_labelExist)
        //     return _labelExist
        // })

        // return flag
        var numbers = [1, 4, 9];
        var dic_number = {"one":1, "two":2, "three":3}
        // var doubles = dic_number.map(i, function(num) {
        //     console.log(num)
        //     return num * 2;
        // });

        let flag = this.state.cellfeature
        console.log(flag)
        for (let [k, v] of Object.entries(flag)) {
            // do something with k and v
            console.log(k)
            console.log(v)
        } 
    }
    getDataFrameType () {
        console.log("ChildGetDataFrameType"); 
        if (!this.props.WdnnTableColumnType) {return null;}
    	
        for (let[k,v] of Object.entries(this.props.WdnnTableColumnType)){
            console.log(k); 
            console.log(v);
            }
        
     }

    setWdnnTableColumnType()
    {
        console.log("setWdnnTableColumnType")
        //this.celHeaderSelectBoxValue = this.props.WdnnTableColumnType
        console.log(this.props.WdnnTableColumnType)
        console.log(this.celHeaderSelectBoxValue)
        
        //console.log(this.celHeaderSelectBoxValue["SI"]["column_type"])
        //this.setState({celStateHeaderSelectBoxValue:this.props.WdnnTableColumnType}) 

        this.props.reportRepository.getDataFrameOnNetworkConfig().then((resultData) => {
            console.log('dataframepost results end');
            this.setState({WdnnTableColumnType: resultData['result']});
            this.celHeaderSelectBoxValue = resultData['result'];
            console.log("setWdnnTableColumnType")
            // for (let[k,v] of Object.entries(resultData['result'])){
            //     console.log(k); 
            //     console.log(v);
            // }
        });
        
    }

    // getCategoryType(columnValues)
    // {
    //     let _celHeaderSelectBoxValue = {}
    //     let _celHeaderSelectBox = {}
        
    //     try{
    //         console.log("hasValue")
    //         console.log(columnValues)
    //         console.log(this.celHeaderSelectBoxValue)
    //         console.log(this.WdnnTableColumnType)
    //         //console.log(this.state.celStateHeaderSelectBoxValue)
    //         //debugger
    //        // console.log(this.state.celStateHeaderSelectBoxValue[columnValues])
    //         //console.log(this.props.WdnnTableColumnType[columnValues])
    //         _celHeaderSelectBoxValue["column_type"] = this.celHeaderSelectBoxValue[columnValues]["column_type"]
    //     }catch(e)
    //     {
    //         console.log("catch")
    //         console.log(columnValues)
    //        _celHeaderSelectBoxValue["column_type"] = "NONE"
    //     }
    //     _celHeaderSelectBox[columnValues] = _celHeaderSelectBoxValue
    //     this.celHeaderSelectBoxValue = _celHeaderSelectBox
    //     // for (let k of _celHeaderSelectBox){
    //     //     console.log("getCategoryType")
    //     //     console.log(k)
    //     // }

    //     console.log(_celHeaderSelectBox[columnValues])
    //     //return _celHeaderSelectBox[columnValues]
    //     return this.celHeaderSelectBoxValue[columnValues]
    // }
    getCategoryType2(WdnnTableColumnType)
    {
        let _celHeaderSelectBoxValue = {}
        let _celHeaderSelectBox = {}
        let _WdnnTableColumnType = {}
        console.log(this.first_time)
        if (this.first_time == true){
            console.log("WdnnTableColumnType true")
            _WdnnTableColumnType = WdnnTableColumnType
        }else{
            console.log("celHeaderSelectBoxValue false")
            _WdnnTableColumnType = this.celHeaderSelectBoxValue
        }

        // for(let [k,v] of Object.entries(_WdnnTableColumnType))
        // {
        //     console.log(k); 
        //     console.log(v);
        //     console.log("getCategoryType2");

        // }

        for(let columnValues of this.props.WdnnTableData[0])
        {
            try{
            console.log("hasValue")
            //console.log(columnValues)
            //console.log(this.celHeaderSelectBoxValue)
            //console.log(_WdnnTableColumnType[columnValues]["column_type"])
            //console.log(this.state.celStateHeaderSelectBoxValue)
            //debugger
           // console.log(this.state.celStateHeaderSelectBoxValue[columnValues])
            //console.log(this.props.WdnnTableColumnType[columnValues])
            _celHeaderSelectBoxValue["column_type"] = _WdnnTableColumnType[columnValues]["column_type"]
            }catch(e)
            {
                console.log("catch")
                console.log(columnValues)
            _celHeaderSelectBoxValue["column_type"] = "NONE"
            }
            _celHeaderSelectBox[columnValues] = _celHeaderSelectBoxValue

        }
        this.celHeaderSelectBoxValue = _celHeaderSelectBox
        //let sdfsdsdsf = this.props.WdnnTableData[0]
        //console.log("wddtabledata")
        //console.log(sdfsdsdsf)

        //this.celHeaderSelectBoxValue = _celHeaderSelectBox
        // for (let k of _celHeaderSelectBox){
        //     console.log("getCategoryType")
        //     console.log(k)
        // }

       // console.log(_celHeaderSelectBox[columnValues])
        //return _celHeaderSelectBox[columnValues]
        this.first_time =false
        console.log("it should be false")
        console.log(this.first_time)
        return this.celHeaderSelectBoxValue
    }
    getCategoryType3(WdnnTableColumnType)
    {
        if (!this.props.WdnnTableColumnType) {
            console.log("props.WdnnTableColumnType is null")
            let column_type = {}
            let row_column_type = {}
            //var key = Object.keyAt(this.props.WdnnTableData, 0);
            //var val = this.props.WdnnTableData[key];

            //console.log(key); // => 'bar'
            //console.log(val); // => '2nd'
            console.log(this.props.WdnnTableData)
           // console.log(Object.keys(this.props.WdnnTableData)[0]); // "a"

            // let opt_url =  this.props.baseDom + '/table/' + this.props.tableDom + '/data/'
            // this.props.reportRepository.getWdnnTableDataFromHbase(opt_url).then((tableData) => {
            //     console.log('data configuration search end')
            // this.setState({WdnnTableData: tableData['result']})
            // });

            this.celHeaderSelectBoxValue2 = null
        }
        else{
            console.log("console.log( props.WdnnTableColumnType is null has value")
            let _celHeaderSelectBoxValue = {}
            let _celHeaderSelectBox = {}
            let _WdnnTableColumnType = {}
            console.log(this.first_time)
            if (this.first_time == true){
                console.log("WdnnTableColumnType true")
                _WdnnTableColumnType = this.props.WdnnTableColumnType
            }else{
                console.log("celHeaderSelectBoxValue false")
                _WdnnTableColumnType = this.celHeaderSelectBoxValue
            }

            this.first_time =false
            console.log("it should be false")
            console.log(this.first_time)
            this.celHeaderSelectBoxValue2 = _WdnnTableColumnType 
        }
        return this.celHeaderSelectBoxValue2
    }


    render() {
    	console.log("calling MetaStore_Table")
        let metaStoreTableContent = [];
    	let i=0;
        let j=0;
        let k=0;
        //let tableHeaderCategory = []; //make Category
        let tableHeader = []; //make header
        let tableData = []; // make tabledata

        let noneSelected = null;
        let cateSelected = null;
        let contiSelected = null;
        let labelSelected = null;
        let getColumnType = {};
        console.log("wdddtablecolumnType")
        console.log(this.props.WdnnTableColumnType)
        //뭔가 한번만
        //this.celHeaderSelectBoxValue2 = this.props.WdnnTableColumnType

        //console.log("#############################################")
        //console.log(this.celHeaderSelectBoxValue)


        //getColumnType =    this.getDataFrameType()
        if(!this.props.WdnnTableData){
            return (<div></div>)
        }

		for(let rows of this.props.WdnnTableData){

            let celHeaderCategory = [];
            let celHeaderCategory1 = [];
            let celHeaderCategory2 = [];
            let celHeader = [];
            let celData = [];
			for(let columnValues of rows){
                //add colums
                if( j==0 ){
                    let celHeaderCategoryTypeNone = [];
                    let celHeaderCategoryTypeConti = [];
                    let celHeaderCategoryTypeCate = [];
                    let celHeaderCategoryTypelabel = [];
                    //this.setState({celStateHeaderSelectBoxValue : null})
                    //this.celHeaderSelectBoxValue = {};
                    //let celHeaderSelectBoxValue = {};
                    // console.log(columnValues)
                    // try{
                    //     console.log(this.props.WdnnTableColumnType[columnValues]["column_type"])
                    // }catch(e)
                    // {
                    //     console.log("catch")
                    //     console.log(this.props.WdnnTableColumnType[columnValues])
                    // }   

                    // //column_type       
                    //column_type
                    //this.celHeaderSelectBoxValue = this.props.WdnnTableColumnType
                    // try{                        
                    //     if("CONTINUOUS"==this.props.WdnnTableColumnType[columnValues]["column_type"]){
                    //         console.log("RendercontiSelected")
                    //         this.celHeaderSelectBoxValue[columnValues] = "CONTINUOUS"
                    //     }else if("CATEGORICAL"==this.props.WdnnTableColumnType[columnValues]["column_type"]){
                    //         console.log("RendercateSelected")
                    //         this.celHeaderSelectBoxValue[columnValues] = "CATEGORICAL"
                    //     }else if("LABEL"==this.props.WdnnTableColumnType[columnValues]["column_type"]){
                    //         console.log("RenderlabelSelected")
                    //         this.celHeaderSelectBoxValue[columnValues] = "LABEL"            
                    //     }
                    // }catch(e)
                    // {
                    //     console.log("catch")
                    //     this.celHeaderSelectBoxValue[columnValues] = "NONE"

                    // } 

                    // try{                        
                    //     if("CONTINUOUS"==this.celStateHeaderSelectBoxValue[columnValues]["column_type"]){
                    //         console.log("RendercontiSelected")
                    //         this.celHeaderSelectBoxValue[columnValues] = "CONTINUOUS"
                    //     }else if("CATEGORICAL"==this.celStateHeaderSelectBoxValue[columnValues]["column_type"]){
                    //         console.log("RendercateSelected")
                    //         this.celHeaderSelectBoxValue[columnValues] = "CATEGORICAL"
                    //     }else if("LABEL"==this.celStateHeaderSelectBoxValue[columnValues]["column_type"]){
                    //         console.log("RenderlabelSelected")
                    //         this.celHeaderSelectBoxValue[columnValues] = "LABEL"            
                    //     }
                    // }catch(e)
                    // {defaultValue={this.celHeaderSelectBoxValue2[columnValues]["column_type"]}
                    //     console.log("catch")
                    //     this.celHeaderSelectBoxValue[columnValues] = "NONE"
                    // id={columnValues} defaultValue={this.celHeaderSelectBoxValue2[columnValues]["column_type"]} >

                    // } 
                    //celHeaderCategory1.push(<select ref="s1" onChange={this.handleChange.bind(this)} id={columnValues}>  {}</select>)
   
                    if (this.celHeaderSelectBoxValue2 && this.celHeaderSelectBoxValue2[columnValues]){

                  
                     celHeaderCategory.push(    <td key={k++}>
                                                    <div className="option-select">
                                                    <select ref="s1" onChange={this.handleChange.bind(this)}
                                                           id={columnValues} defaultValue={this.celHeaderSelectBoxValue2[columnValues]["column_type"]}>
                                                       <option value="NONE">None</option>
                                                       <option  value="CATEGORICAL">Category Type</option>
                                                       <option value="CONTINUOUS">Continuous Type</option>
                                                       <option  value="LABEL">Label</option>
                                                    </select>
                                                    </div>
                                                </td>)
                    }else{
                                  celHeaderCategory.push(    <td key={k++}>
                                                    <div className="option-select">
                                                    <select ref="s1" onChange={this.handleChange.bind(this)}
                                                           id={columnValues} >
                                                       <option value="NONE">None</option>
                                                       <option  value="CATEGORICAL">Category Type</option>
                                                       <option value="CONTINUOUS">Continuous Type</option>
                                                       <option  value="LABEL">Label</option>
                                                    </select>
                                                    </div>
                                                </td>)
                    }

                    // celHeaderCategory.push(    <td key={k++}>
                    //                                 <div className="option-select">
                    //                                 <select onChange={this.handleChange.bind(this)}
                    //                                         id={columnValues} >   
                    //                                     {celHeaderCategoryTypeNone}
                    //                                     {celHeaderCategoryTypeConti}
                    //                                     {celHeaderCategoryTypeCate}
                    //                                     {celHeaderCategoryTypelabel}
                    //                                 </select>
                    //                                 </div>
                    //                             </td>)
                    celHeader.push(<th key={i++} > {columnValues}</th>)
                }else{
                    celData.push(<td key={i++} > {columnValues}</td>)
                }
			}
            //add rows
            if(j==0){
                tableHeader.push(<tr className="option-select" key={j++}>{celHeaderCategory}</tr>)
                tableHeader.push(<tr key={j++}>{celHeader}</tr>)
            }else{
                tableData.push(<tr key={j++}>{celData}</tr>)
            }
		}
        //add table 
        metaStoreTableContent.push(<thead key={j++}>{tableHeader}</thead>)
        metaStoreTableContent.push(<tbody key={j++} className="center">{tableData}</tbody>)
        
        return (   
            <div>
                <table className="table marginT10">
                    {metaStoreTableContent}
                </table>
            </div>        
        )
    }
}
MetaStore_TableLayout.defaultProps = {
    reportRepository: new ReportRepository(new Api())
};
