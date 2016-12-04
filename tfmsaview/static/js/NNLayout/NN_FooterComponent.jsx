import React from 'react'

export default class NN_FooterComponent extends React.Component {
    render() {
        return (   
			<footer>
{/* sub 페이지 반영 활성화시 main tag에 sub_main 클레스 추가되야 함 sub 페이지 반영
                    <div className="console_wrap">
                        <div className="console_area">
                            <dl className="console_list">
                                <dt>ID:</dt>
                                <dd>Mes_m20_cifar_53702</dd>
                            </dl>
                            <dl className="console_list">
                                <dt>Category:</dt>
                                <dd>Mes</dd>
                            </dl>
                            <dl className="console_list">
                                <dt>Type:</dt>
                                <dd>cifar</dd>
                            </dl>
                            <dl className="console_list">
                                <dt>Title:</dt>
                                <dd>CIFAR TEST</dd>
                            </dl>
                        </div>
                    </div>
*/}
                    <footer>
                        <div className="copyright_area">
                            Copyrights ⓒ POSCO ICT. All rights reserved. 
                        </div>
                    </footer>
			</footer>
        )
    }
}