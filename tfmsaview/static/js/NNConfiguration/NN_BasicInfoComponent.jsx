import React from 'react';

export default class NN_BasicInfoComponent extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
                <section>
                    <h1 className="hidden">tensor MSA main table</h1>
                    <ul className="tabHeader">
                        <li className="current"><a href="#">Network Basic Information</a></li>
                        <div className="btnArea">
                            <button type="button">Upload</button>
                            <button type="button">Save</button>
                        </div>
                    </ul>   
                        <div className="container tabBody">
                            <div id="tab1">
                                <article>
                                    <table className="form-table align-left">
                                        <colgroup>
                                        <col width="250" />
                                        <col width="500" />
                                        <col width="250" />
                                        <col width="500" />
                                        </colgroup> 
                                        <tbody>
                                        <tr>
                                            <th>GROUP(Business Category)</th>
                                            <td>
                                                <select>
                                                    <option value="1">GROUP(Business Category)</option>
                                                    <option value="2"></option>
                                                </select>
                                            </td>
                                            <th>Neural Network Type</th>
                                            <td>
                                                <select>
                                                <option value="1">Neural Network Type</option>
                                                <option value="2"></option>
                                                </select>
                                            </td>
                                        </tr>
                                        <tr>
                                            <th>Title</th>
                                            <td colSpan="3"><input type="text" className="w100p"></input></td>
                                        </tr>
                                        <tr>
                                            <td colSpan="4">
                                                <span className="label-blue positionA">Description</span>
                                                <textarea rows="30" className="w100p paddingT30"></textarea>
                                            </td>
                                        </tr>
                                        </tbody>
                                    </table>
                                </article>
                            </div>
                        </div>
                </section>
        )
    }
}