"""
Active shape model automatic segmentation
implemented in GIAS and using Fieldwork models.
"""
import numpy as np
import time

from gias2.image_analysis import fw_segmentation_tools as fst
from gias2.image_analysis import asm_segmentation as ASM


class ParameterError(Exception):
    pass


def segment(scan, model, shapepcs, config):
    # parse configs
    verbose = config['general']['verbose']
    if verbose:
        print(config)

    flipX = config['image']['flip_x']
    flipY = config['image']['flip_y']
    flipZ = config['image']['flip_z']
    NEGSPACING = config['image']['neg_spacing']
    ZSHIFT = config['image']['z_shift']

    PPCFilename = config['data_files']['ppc_filename']
    if PPCFilename is None:
        raise ParameterError('PPCFilename not set')

    asmConfigs = config['ASM']
    asmShapeModes = asmConfigs['shape_modes']
    asmParams = ASM.ASMSegmentationParams(**{
        'PPCFilename': PPCFilename,
        'GD': asmConfigs['mesh_d'],
        'ND': asmConfigs['n_d'],
        'NLim': asmConfigs['n_lim'],
        'NPad': asmConfigs['n_pad'],
        'matchMode': asmConfigs['match_mode'],
        'MDistWeight': asmConfigs['m_dist_weight'],
        'MDistWeightUpper': asmConfigs['m_dist_weight_upper'],
        'PPCVarCutoff': asmConfigs['ppc_var_cutoff'],
        'passWindow': asmConfigs['pass_window'],
        'minPassFrac': asmConfigs['min_pass_frac'],
        'maxIt': asmConfigs['max_it'],
        'filterLandmarks': asmConfigs['filter_landmarks'],
        'imageZShift': ZSHIFT,
        'imageNegSpacing': NEGSPACING,
        'verbose': verbose,
    })
    asmFitMWeight = asmConfigs['fit_mweight']
    filterLandmarks = asmConfigs['filter_landmarks']
    fitSize = asmConfigs['fit_size']

    # ===========================================================================#
    t0 = time.time()
    tprev = t0

    # initialise image
    if flipX:
        scan.I = scan.I[::-1, :, :]
    if flipY:
        scan.I = scan.I[:, ::-1, :]
    if flipZ:
        scan.I = scan.I[:, :, ::-1]

    # run ASM function
    asmOutput, asm, GF, croppedScan, \
    meshEval, paramsEval, meshFit = fst.doASM(
        asmParams, scan, model, 'PCXiGrid',
        'PCDPEP', asmParams.GD, shapepcs,
        np.arange(asmShapeModes), None,
        asmFitMWeight, verbose=verbose,
        filterLandmarks=filterLandmarks,
        doScale=fitSize,
        landmarkTargets=None,
        landmarkEvaluator=None,
        landmarkWeights=None,
    )

    dataASM = asmOutput['segData']
    meshParamsASM = asmOutput['segXOpt']
    model.set_field_parameters(paramsEval(meshParamsASM))

    if verbose:
        print('ASM done (%5.2fs)' % (time.time() - tprev))

    # unflip image if fliped
    if flipX:
        scan.I = scan.I[::-1, :, :]
    if flipY:
        scan.I = scan.I[:, ::-1, :]
    if flipZ:
        scan.I = scan.I[:, :, ::-1]

    return model, dataASM, meshParamsASM, asmOutput
