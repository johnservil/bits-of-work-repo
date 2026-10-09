"""Regression checks for scientific meaning, not just presentation."""
import importlib.util
import json
import math
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('history', Path(__file__).with_name('attack_stability.py'))
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)


def milestone(year, cost, **kw):
    return dict(year=year, date=str(year), name=str(year), authors='Test', ref='Test source',
                source_url='https://example.org/paper', series=True, status='supported',
                model='classical', cost=cost) | kw


class MeaningTests(unittest.TestCase):
    def test_nonparameterized_models_do_not_invent_work_or_infinite_size(self):
        for kind in ('poly', 'quasipoly'):
            c = {'type': kind, 'log2_ops_at_reference': 42}
            self.assertIsNone(h.log2_cost(c, 434))
            self.assertIsNone(h.size_for(c, 128))

    def test_corrected_claim_cannot_win_running_minimum(self):
        bad = milestone(2018, {'type':'linear','c':.0885}, status='corrected', series=False)
        good = milestone(2022, {'type':'linear','c':.0951})
        p = dict(key='test',display_kind='index',reference={'size':1346},from_year=2018,milestones=[bad,good])
        r = h.analyse(p)
        self.assertEqual(len(r['steps']), 1)
        self.assertAlmostEqual(r['metrics']['current_cost'], 128.0046)
        bad['series'] = True
        with self.assertRaises(ValueError):
            h.analyse(p)

    def test_reference_and_inverse_envelopes_choose_independently(self):
        # The linear bound wins at size 100, while n log n is cheaper near the
        # target threshold and hence imposes the larger required size.
        p = dict(key='test',display_kind='index',reference={'size':100},from_year=2000,
                 milestones=[milestone(2000,{'type':'linear','c':5}),
                             milestone(2001,{'type':'nlogn','c':1})])
        r = h.analyse(p)
        self.assertEqual(r['steps'][-1]['name'], '2000')
        self.assertEqual(r['size_steps'][-1]['name'], '2001')
        self.assertGreater(r['metrics']['current_size'], 128/5)

    def test_rsa_index_uses_exact_one_third(self):
        c = {'type':'L','a':1/3,'c':(64/9)**(1/3)}
        gap = h.log2_cost(c,2048)-h.log2_cost(c,896)
        self.assertAlmostEqual(gap,35.0241848230,places=7)

    def test_corpus_has_no_unsourced_or_imaginary_event_indices(self):
        for path in h.SRC.glob('*.json'):
            p = json.loads(path.read_text())
            result = h.analyse(p)
            if p['display_kind'] == 'events':
                self.assertIsNone(result['metrics'])
                self.assertEqual(result['steps'], [])
            for m in p['milestones']:
                self.assertTrue(m['source_url'].startswith('https://'))
                if h.in_series(m):
                    self.assertFalse(m.get('verified', False))
                    size = h.size_for(m['cost'],128)
                    self.assertTrue(math.isfinite(size))
                    self.assertAlmostEqual(h.log2_cost(m['cost'],size),128,places=7)


if __name__ == '__main__':
    unittest.main()
