import React from 'react'
import TestUtils from 'react-addons-test-utils'
import {findRenderedDOMComponentWithClass as find} from 'react-addons-test-utils'
import {scryRenderedDOMComponentsWithClass as findAll} from 'react-addons-test-utils'
import HomeComponent from './../js/HomeComponent'
import expect from 'expect'

describe("HomeComponent", function() {
    let renderer = TestUtils.createRenderer();
    renderer.render(<HomeComponent/>);
  	let result = renderer.getRenderOutput();

    it("should display create NN conf", () => {
        let instance = renderer.getMountedInstance();
        instance.case1();
        expect(instance.state.data).toBe(null);
        expect(result.props.children[0].props.children).toBe('Hello TensorMSA');

    //    TestUtils.Simulate.click(find(HomeComponent, 'getAPI1'));
    //   expect(findAll(HomeComponent, 'displayAPI').length).toEqual(0);    

    });

    it("should display Search NN conf", () => {
     //  TestUtils.Simulate.click(find('getAPI'));
     //  expect(result.type).toBe('div');
    });

    it("should display Create Data Table", () => {
     //  TestUtils.Simulate.click(find('getAPI'));
     //  expect(result.type).toBe('div');
    });

    it("should display Search Data Table", () => {
     //  TestUtils.Simulate.click(find('getAPI'));
     //  expect(result.type).toBe('div');
    });
});