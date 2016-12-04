import React from 'react'
import * as d3 from "d3"
import dc from 'dc'
import crossfilter from 'crossfilter'
import '../../../node_modules/dc/dc.css'

export default class LabelByChartComponent extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            chartSection : null
        };
    }

    componentWillMount() {
        this.makeChartDOM();
    }

    componentDidMount() { //after DOM make D3 Chart
        this.makeChart();
    }

    componentDidUpdate() { 
        if(this.state.chartSection == null){
            this.makeChartDOM();
        }
        this.makeChart();
    }

    makeChart(){ 
        const chartSection1 = [];
        let section = d3.keys(this.props.data);
        for (const numSection of section){
            this.createChart(numSection, this.props.data);
        }
    }

    makeChartDOM(){
        const chartSection1 = [];
        let section = d3.keys(this.props.data);
        for (const numSection of section){
            chartSection1.push(<dl className='data-box' key = {numSection}>
                                <dt><span>{numSection}</span></dt>
                                <dd id={"_" + numSection}></dd>
                            </dl>);
        }
        this.setState({chartSection: chartSection1});   
    }

    createChart(section, allData){
            let data = allData[section];
            let chart = dc.pieChart('#_' + section,'_' + section);
            let ndx           = crossfilter(data);
            let Dimension  = ndx.dimension(function(d) {return d.label;});
            let dataGroup = Dimension.group().reduceSum(function(d) {return d.value;});

            chart
                .width(200)
                .height(200)
                .innerRadius(0)
                .dimension(Dimension)
                .ordinalColors(['#2E8B57', '#DC143C'])
                .transitionDuration(1500) //add animation speed
                .group(dataGroup);
            chart.render('_' + section);
    }

    render() {
        return (   
                    <article>
                        {this.state.chartSection}
                    </article>
        )
    }
}