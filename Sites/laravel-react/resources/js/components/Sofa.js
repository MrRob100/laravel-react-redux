import React from 'react';
import Cushion from "./Cushion";

function Sofa() {
    return (
        <div className="container">
            <div className="row justify-content-center my-3">
                <div className="col-md-8">
                    <div className="card">
                        <div className="card-header">Sofa</div>
                        <div className="card-body">
                            <Cushion/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Sofa;
