import React from 'react';
import ReactDOM from 'react-dom';
import Sofa from "./Sofa";
import rootReducer from "../reducers"
import { Prodiver } from 'react-redux'

import {createStore, combineReducers} from 'redux';

const store = createStore(rootReducer);

// ACTION
const increment = () => {
    return {
        type: 'INCREMENT'
    }
}

const decrement = () => {
    return {
        type: 'DECREMENT'
    }
}

//Show in the console
store.subscribe(() => console.log(store.getState()));

//DISPATCH
store.dispatch(increment());
store.dispatch(decrement());
store.dispatch(decrement());

//Display

function Shop() {
    return (
        <div className="container">
            <div className="row justify-content-center">
                <div className="col-md-8">
                    <div className="card">
                        <div className="card-header">Shop</div>
                        <div className="card-body">
                            <Sofa/>
                            <Sofa/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Shop;

if (document.getElementById('shop')) {
    ReactDOM.render(<Shop />, document.getElementById('shop'));
}
