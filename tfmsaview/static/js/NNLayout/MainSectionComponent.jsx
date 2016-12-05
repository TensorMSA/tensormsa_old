import React from 'react'

export default class MainSectionComponent extends React.Component {
    render() {
        return (   
                <section>
	            	<div className="main_visual_area">
						<ul className="visual_img">
							<li><img src="images/main_visual01.jpg" alt="" /></li>
							<li className="on"><img src="images/main_visual02.jpg" alt=""/></li>
						</ul>
						<div className="visual_txt_area">
							<p className="visual_txt">
								<strong>Hoya is a Machine Intelligence</strong>
								Framework Based on Tensorflow
							</p>
							<a href="#none">JOB START!</a>
						</div>
					</div>
                </section>
        )
    }
}