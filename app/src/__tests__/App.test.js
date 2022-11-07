/**
 * @vitest-environment jsdom
 */
import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import App from '../App.vue';
//base test to make sure App.vue is rendering
describe('HelloWorld', () => {
    it('renders properly', () => {
      const wrapper = mount(App);
      expect(wrapper.text()).toContain('Hello Vitest');
    })
  })