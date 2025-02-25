# model settings
model = dict(
    type='S2ANet',
    backbone=dict(
        type='Resnet50',
        frozen_stages=1,
        return_stages=["layer1", "layer2", "layer3", "layer4"],
        pretrained=True),
    neck=dict(
        type='FPN',
        in_channels=[256, 512, 1024, 2048],
        out_channels=256,
        start_level=1,
        add_extra_convs="on_input",
        num_outs=5),
    bbox_head=dict(
        type='S2ANetHead',
        num_classes=2,
        in_channels=256,
        feat_channels=256,
        stacked_convs=2,
        with_orconv=True,
        anchor_ratios=[1.0],
        anchor_strides=[8, 16, 32, 64, 128],
        anchor_scales=[4],
        target_means=[.0, .0, .0, .0, .0],
        target_stds=[1.0, 1.0, 1.0, 1.0, 1.0],
        loss_fam_cls=dict(
            type='FocalLoss',
            use_sigmoid=True,
            gamma=2.0,
            alpha=0.25,
            loss_weight=1.0),
        loss_fam_bbox=dict(
            type='SmoothL1Loss', beta=1.0 / 9.0, loss_weight=1.0),
        loss_odm_cls=dict(
            type='FocalLoss',
            use_sigmoid=True,
            gamma=2.0,
            alpha=0.25,
            loss_weight=1.0),
        loss_odm_bbox=dict(
            type='SmoothL1Loss', beta=1.0 / 9.0, loss_weight=1.0),
        test_cfg=dict(
            nms_pre=2000,
            min_bbox_size=0,
            score_thr=0.3,
            nms=dict(type='nms_rotated', iou_thr=0.1),
            max_per_img=2000),
        train_cfg=dict(
            fam_cfg=dict(
                assigner=dict(
                    type='MaxIoUAssigner',
                    pos_iou_thr=0.5,
                    neg_iou_thr=0.4,
                    min_pos_iou=0,
                    ignore_iof_thr=-1,
                    iou_calculator=dict(type='BboxOverlaps2D_rotated')),
                bbox_coder=dict(type='DeltaXYWHABBoxCoder',
                                target_means=(0., 0., 0., 0., 0.),
                                target_stds=(1., 1., 1., 1., 1.),
                                clip_border=True),
                allowed_border=-1,
                pos_weight=-1,
                debug=False),
            odm_cfg=dict(
                assigner=dict(
                    type='MaxIoUAssigner',
                    pos_iou_thr=0.5,
                    neg_iou_thr=0.4,
                    min_pos_iou=0,
                    ignore_iof_thr=-1,
                    iou_calculator=dict(type='BboxOverlaps2D_rotated')),
                bbox_coder=dict(type='DeltaXYWHABBoxCoder',
                                target_means=(0., 0., 0., 0., 0.),
                                target_stds=(1., 1., 1., 1., 1.),
                                clip_border=True),
                allowed_border=-1,
                pos_weight=-1,
                debug=False))
    )
)
dataset = dict(
    train=dict(
        type="OCRDataset",
        dataset_dir='/home/gmh/dataset/dataset/dataset/dataset2',
        img_dir='1306',
        gt_dir='1306',
        transforms=[
            dict(
                type="RotatedResize",
                min_size=630,
                max_size=1120,
            ),
            dict(type='RotatedRandomFlip', prob=0.5),
            dict(
                type="Pad",
                size_divisor=32),
            dict(
                type="Normalize",
                mean=[123.675, 116.28, 103.53],
                std=[58.395, 57.12, 57.375],
                to_bgr=False,)

        ],
        batch_size=4,
        num_workers=4,
        shuffle=True,
        filter_empty_gt=False
    ),
    val=dict(
        type="OCRDataset",
        dataset_dir='/home/gmh/dataset/dataset/dataset/dataset2',
        img_dir='1306',
        gt_dir='1306',
        transforms=[
            dict(
                type="RotatedResize",
                min_size=630,
                max_size=1120,
            ),
            dict(
                type="Pad",
                size_divisor=32),
            dict(
                type="Normalize",
                mean=[123.675, 116.28, 103.53],
                std=[58.395, 57.12, 57.375],
                to_bgr=False),
        ],
        batch_size=2,
        num_workers=4,
        shuffle=False
    ),
    test=dict(
        type="ImageDataset",
        images_dir='/home/gmh/dataset/dataset/dataset/dataset2/imgs',
        transforms=[
            dict(
                type="RotatedResize",
                min_size=630,
                max_size=1120,
            ),
            dict(
                type="Pad",
                size_divisor=32),
            dict(
                type="Normalize",
                mean=[123.675, 116.28, 103.53],
                std=[58.395, 57.12, 57.375],
                to_bgr=False),
        ],
        batch_size=1,
        num_workers=4,
    )
)

optimizer = dict(
    type='SGD',
    lr=0.01/4.,  # 0.0,#0.01*(1/8.),
    momentum=0.9,
    weight_decay=0.0001,
    grad_clip=dict(
        max_norm=35,
        norm_type=2))

# learning policy
scheduler = dict(
    type='StepLR',
    warmup='linear',
    warmup_iters=500,
    warmup_ratio=1.0 / 3,
    milestones=[35, 50])

# yapf:disable
logger = dict(
    type="RunLogger")
# yapf:enable
# runtime settings
max_epoch = 60
eval_interval = 6
checkpoint_interval = 1
log_interval = 20
