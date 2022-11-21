/**
 * @vitest-environment happy-dom
 */
 import { describe, it, expect } from 'vitest';
 import { mount } from '@vue/test-utils';
 import ResultsComponent from 'src/components/ResultsComponent.vue';

 // tests the result comonent, what result is shown
describe('show RESULTS!', () => {
    it('should render page', () =>{
        const wrapper = mount(ResultsComponent, {
            propsData: {
              results: []
            }
          })
        expect(wrapper.find('div').exists()).toBeTruthy()
    });
    // it('should change results', asynch() => {
    //     const wrapper = mount(ResultsComponent)
    //     await wrapper.find('button').trigger('click')
    //     expect(wrapper.find('h1'.text()).toEqual('1:09pm-3:01pm 1h 58min 1 $170 hi'))
    // })
})