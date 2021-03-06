import numpy as np
from ._masker import Masker

class FixedComposite(Masker):
    def __init__(self, masker):
        """ Creates a Composite masker from an underlying masker and returns the original args along with the masked output.

        Parameters
        ----------
        masker: object
            An object of the shap.maskers.Masker base class (eg. Text/Image masker).

        Returns
        -------
        tuple
            A tuple consisting of the masked input using the underlying masker appended with the original args in a list.
        """
        self.masker = masker
        # define attributes to be dynamically set
        masker_attributes = ["shape", "invariants", "clustering", "data_transform", "mask_shapes", "feature_names"]
        # set attributes dynamically
        for masker_attribute in masker_attributes:
            if getattr(self.masker, masker_attribute, None) is not None:
                setattr(self, masker_attribute, getattr(self.masker, masker_attribute))

    def __call__(self, mask, *args):
        """ Computes mask on the args using the masker data attribute and returns tuple containing masked input with args.
        """
        masked_X = self.masker(mask, *args)
        wrapped_args = []
        for item in args:
            wrapped_args.append(np.array([item]))
        wrapped_args = tuple(wrapped_args)
        if not isinstance(masked_X, tuple):
            masked_X = (masked_X,)
        return masked_X + wrapped_args
    