/**
 * Input & Form Data Validation Utility
 */

export function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(String(email).toLowerCase());
}

export function validatePassword(password) {
  return typeof password === 'string' && password.length >= 6;
}

export function validateSubmission(formData) {
  const errors = {};

  if (!formData.title || formData.title.trim().length < 3) {
    errors.title = 'Title must be at least 3 characters long.';
  }

  if (!formData.category) {
    errors.category = 'Please select a design category.';
  }

  if (!formData.description || formData.description.trim().length < 10) {
    errors.description = 'Description must be at least 10 characters long.';
  }

  if (formData.previewImageFile) {
    const validImageTypes = ['image/jpeg', 'image/png', 'image/webp', 'image/gif', 'image/svg+xml'];
    if (!validImageTypes.includes(formData.previewImageFile.type)) {
      errors.previewImage = 'Preview must be a valid image file (JPG, PNG, WebP, GIF, SVG).';
    }
    if (formData.previewImageFile.size > 5 * 1024 * 1024) {
      errors.previewImage = 'Image size must be less than 5MB.';
    }
  }

  if (formData.zipPackageFile) {
    const isZip = formData.zipPackageFile.type === 'application/zip' ||
                  formData.zipPackageFile.type === 'application/x-zip-compressed' ||
                  formData.zipPackageFile.name.endsWith('.zip');
    if (!isZip) {
      errors.zipPackage = 'Uploaded file must be a valid .ZIP package.';
    }
    if (formData.zipPackageFile.size > 25 * 1024 * 1024) {
      errors.zipPackage = 'ZIP archive must be under 25MB.';
    }
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
}
