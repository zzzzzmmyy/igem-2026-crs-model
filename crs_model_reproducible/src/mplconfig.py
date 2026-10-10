"""Use a headless plotting backend; each figure scopes its own visual style."""
import matplotlib

matplotlib.use("Agg")
