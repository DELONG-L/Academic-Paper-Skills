"""Exercise configurable plotting dimensions and real export behavior."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import matplotlib.pyplot as plt
from paperfig_style import FigureStyle, create_figure, grouped_bar, save_figure
from setup_style import setup_style


class PlotConfigurationTests(unittest.TestCase):
    def test_explicit_manuscript_width_and_font_reach_render(self):
        with plt.rc_context():
            style = FigureStyle(font_size=10, label_size=11, tick_size=9, legend_size=9)
            fig, axes = create_figure(width_inches=4.1, height_ratio=0.7, style=style)
            self.addCleanup(plt.close, fig)
            self.assertAlmostEqual(4.1, fig.get_figwidth())
            self.assertAlmostEqual(4.1 * 0.7, fig.get_figheight())
            grouped_bar(axes[0], ['A', 'B'], [[2, 4]], ['Example'], annotate=True)
            fig.canvas.draw()
            self.assertEqual(['2.00', '4.00'], [t.get_text() for t in axes[0].texts])
            self.assertTrue(all(t.get_fontsize() == 10 for t in axes[0].texts))
            with TemporaryDirectory() as directory:
                paths = save_figure(fig, Path(directory) / 'example', formats=['pdf', 'svg'])
                self.assertTrue(paths[0].read_bytes().startswith(b'%PDF'))
                self.assertIn('<svg', paths[1].read_text())

    def test_preset_allows_actual_template_overrides(self):
        with plt.rc_context():
            info = setup_style(use_sciplots=False, rc_overrides={
                'figure.figsize': (4.1, 2.7), 'font.size': 10, 'axes.labelsize': 11})
            self.assertEqual([4.1, 2.7], info['figure_size_inches'])
            self.assertEqual(10, plt.rcParams['font.size'])
            self.assertEqual(11, plt.rcParams['axes.labelsize'])

    def test_invalid_placement_fails_before_plotting(self):
        with self.assertRaisesRegex(ValueError, 'dimensions must be positive'):
            create_figure(width_inches=-1)


if __name__ == '__main__':
    unittest.main()
