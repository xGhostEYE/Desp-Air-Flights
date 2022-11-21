/**
 * @vitest-environment jsdom
 */
import { beforeEach, describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import SearchComponent from 'src/components/SearchComponent.vue';

const elementIDs = {
    inputs: ["starting", "destination"],
    errorMessages: ["starting err", "destination err"],
    labels: ["starting label", "destination label"]
};



const validAirports = ["YXE - Saskatoon","LAX - Los Angeles"];
const invalidAirports = ["this should not work", "123", "heck"];


describe.each([
    { id: "starting" },
    { id: "destination" }
])("SearchComponent - Inputs - Testing $id", ({id})=>{
    it('should render page with input ' + id, () =>{
        const wrapper = mount(SearchComponent, {
            propsData: {
              airports: validAirports
            }
          });
        expect(wrapper.find('div').exists()).toBeTruthy();
        expect(wrapper.find('#' + id).exists()).toBeTruthy();
        expect(wrapper.find('#' + id).element.id).toEqual(id);
    });


    it.each(validAirports)('test valid data',(airport)=>{
        const wrapper = mount(SearchComponent, {
            propsData: {
              airports: validAirports
            }
          });
        const input = wrapper.find('#' + id);
        expect(input.exists()).toBeTruthy();
        input.setValue(airport);
        expect(input.element.value).toBe(airport)
        const err = wrapper.find('#' + id + 'Err');
        expect(err.isVisible()).toBeFalsy();
    })


    it.each(invalidAirports)('test invalid data',(airport)=>{
        const wrapper = mount(SearchComponent, {
            propsData: {
              airports: validAirports
            }
          });
        const input = wrapper.find('#' + id);
        expect(input.exists()).toBeTruthy();
        input.setValue(airport);
        expect(input.element.value).toBe(airport);
        const err = wrapper.find('#' + id + 'Err');
        expect(err.isVisible()).toBeTruthy();
    })

    

    // describe("stuff", ()=>{

    // });
    // loop to test that each element it rendering
    // for (const e in elementIDs) {
    //     for (const id in e.inputs) {
    //         it('should render element ' + e + ' with ID: ' + id, () =>{
    //             const wrapper = mount(SearchComponent, {
    //                 propsData: {
    //                 airports: airports.valid[0]
    //                 }
    //             });
    //             expect(wrapper.find('#' + id).exists()).toBeTruthy();
    //             expect(wrapper.find('#' + id).element.id).toEqual("4");
    //         });
    // }
    // }
    // it('should render element with ID: starting', () =>{
    //     const wrapper = mount(SearchComponent, {
    //         propsData: {
    //           airports: airports.valid[0]
    //         }
    //       });
    //     expect(wrapper.find('#starting').exists()).toBeTruthy();
    //     expect(wrapper.find('#starting').element.id).toEqual("4");
    // });
    
    // for (const type in airports) {
    //     for (const airport in type) {
    //         const isValid = type=='valid';
    //         it('testing ' + type + ' data being entered into ' + , () =>{
    //             const wrapper = mount(SearchComponent)
    //             expect(wrapper.find('p').exists()).toBeTruthy()
    //         });
    //     }
    // }
    

    // it('should render page', () =>{
    //     const wrapper = mount(SearchComponent)
    //     expect(wrapper.find('p').exists()).toBeTruthy()
    // });
});



//  describe('SearchComponent Test', () =>{
//     it('should render', () =>{
//         const wrapper = mount(SearchComponent)
//         expect(wrapper.find('p').exists()).toBeTruthy()
//         expect(wrapper.find('button').exists()).toBeTruthy()
//         expect(wrapper.find('div').exists()).toBeTruthy()
//     })

//     it('should show result', async() =>{
//         const wrapper = mount(SearchComponent)
//         await wrapper.find('button').trigger('click')
//         expect(wrapper.find('div').text()).toEqual('StartingDestinationSearch')
//     })


//  })