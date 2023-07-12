import numpy as np

# You are not allowed to use any ML libraries e.g. sklearn, scipy, keras, tensorflow etc

# SUBMIT YOUR CODE AS A SINGLE PYTHON (.PY) FILE INSIDE A ZIP ARCHIVE
# THE NAME OF THE PYTHON FILE MUST BE submit.py
# DO NOT INCLUDE OTHER PACKAGES LIKE SKLEARN, SCIPY, KERAS,TENSORFLOW ETC IN YOUR CODE
# THE USE OF ANY MACHINE LEARNING LIBRARIES WILL RESULT IN A STRAIGHT ZERO

# DO NOT CHANGE THE NAME OF THE METHOD my_fit BELOW
# THESE WILL BE INVOKED BY THE EVALUATION SCRIPT. CHANGING THESE NAMES WILL CAUSE EVALUATION FAILURE

# You may define any new functions, variables, classes here
# For example, functions to calculate next coordinate or step length
def HT( v, k ):
    t = np.zeros_like( v )
    if k < 1:
        return t
    else:
        ind = np.argsort( abs( v ) )[ -k: ]
        t[ ind ] = v[ ind ]
        return t
################################
# Non Editable Region Starting #
################################
def my_fit( X_trn, y_trn ):
################################
#  Non Editable Region Ending  #
################################

    # Use this method to train your model using training CRPs
    # Youe method should return a 2048-dimensional vector that is 512-sparse
    # No bias term allowed -- return just a single 2048-dim vector as output
    # If the vector your return is not 512-sparse, it will be sparsified using hard-thresholding
    model=np.linalg.lstsq(X_trn, y_trn,rcond=None)[0] #initialising the model with the answer to unconstrained optimization problem
    model=HT(model,512) #projecting it to feasible set
    n=X_trn.shape[0] # n stores number of challenge respone pairs in the training data
    step_len=0.01 #step length
    bs=100 #batch size
    for j in range(n):
        indices = np.random.permutation(n) # generating random permutation
        X_trn = X_trn[indices] #re ordering X_trn matrix according to the permutation
        y_trn = y_trn[indices] #re ordering y_trn matrix according to the permutation
        # this ensures the formation of randm batches
        for i in range(0, n, bs):
            #taking batch
            X_batch = X_trn[i:i+bs]
            y_batch = y_trn[i:i+bs]
            #calculating gradient
            grad_ = X_batch.T @ ((X_batch @ model)-y_batch)
            # taking the step in the opposite direction of gradient
            model =model - (step_len/bs) * grad_
            #projecting it to feasible set
            model=(HT(model,512))
        #checking if the norm of Loss function is less then desired value
        if(np.linalg.norm(np.dot(X_trn,model)-y_trn)<=500):
            return model #if so we return the model
    return model                    # Return the trained model

