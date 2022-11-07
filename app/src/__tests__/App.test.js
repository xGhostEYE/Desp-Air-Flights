/**
 * @vitest-environment jsdom
 */
import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import App from '../App.vue';
//base test to make sure tests are working properly
describe('HelloWorld', () => {
    it('renders properly', () => {
      expect("true").toContain('true');
    })
  })