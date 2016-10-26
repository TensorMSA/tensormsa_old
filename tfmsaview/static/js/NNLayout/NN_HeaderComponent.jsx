import React from 'react'

export default class NN_HeaderComponent extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (   
			<header className="mainHeader">
				<h1 className="logo">
					<span className="hidden">tensor MSA</span>
					TensorMSA
				</h1>
				<nav>
					<h1 className="hidden">Navigator</h1>
					<ul>
						<li><a href="#" onClick={() => this.props.getNetInfo()}>Net Info</a></li>
						<li><a href="#" onClick={() => this.props.addNewNNInfo()}>Data</a></li>
						<li><a href="#">Net conf</a></li>
						<li><a href="#">Train Statistics</a></li>
						<li><a href="#">Predict Test</a></li>
					</ul>
				</nav>
				<dl className="utilMenu">
					<dt>Menu</dt>
					<dd><a href="#">help</a></dd>
					<dd><a href="#">logout</a></dd>
					<dd><a href="#"><span>Healess</span>welcome!</a></dd>
				</dl>
			</header>
        )
    }
}