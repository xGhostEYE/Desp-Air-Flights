/**
 * @vitest-environment jsdom
 */
 import { describe, it, expect } from 'vitest';
 import { mount } from '@vue/test-utils';
 import SearchComponent from 'src/components/SearchComponent.vue';

 describe('SearchComponent Test', () =>{
    it('should render', () =>{
        const wrapper = mount(SearchComponent)
        expect(wrapper.find('p').exists()).toBeTruthy()
        // expect(wrapper.find('input[type="text"]').exists()).toBeTruthy()
        expect(wrapper.find('button').exists()).toBeTruthy()
        expect(wrapper.find('div').exists()).toBeTruthy()
    })

    it('should show result', async() =>{
        const wrapper = mount(SearchComponent)
        await wrapper.find('button').trigger('click')
        expect(wrapper.find('div').text()).toEqual('StartingDestinationSearch')
    })


 })