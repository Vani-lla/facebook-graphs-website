import React, { Component, Fragment } from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Graph from './Graph/Graph';
import Main from './Main/Main';
import Status from './Status/Status';

export default class App extends Component {
    render() {
        return (
            <BrowserRouter>
                <Routes>
                    <Route path='/' element={
                        <Fragment>
                            <Main />
                            <Status />
                        </Fragment>
                    } />
                    <Route path='/graph/:id' element={
                        <Fragment>
                            <Graph />
                            <Status />
                        </Fragment>
                    } />
                </Routes >
            </BrowserRouter>
        )
    }


}
