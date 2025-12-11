#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运行所有单元测试
"""

import unittest
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("运行所有单元测试")
    print("=" * 60)

    # 导入测试模块
    try:
        from test_flac_metadata_utils import TestLrcProcessing, TestMetadataProcessing, TestImageProcessing, TestMetadataWrite, TestFlacInfoExtraction, TestIntegration
        from test_video_to_audio import TestVideoToAudio
    except ImportError as e:
        print(f"错误：无法导入测试模块: {e}")
        return False

    # 创建测试套件
    test_suite = unittest.TestSuite()

    # 添加FLAC元数据处理测试
    test_suite.addTest(unittest.makeSuite(TestLrcProcessing))
    test_suite.addTest(unittest.makeSuite(TestMetadataProcessing))
    test_suite.addTest(unittest.makeSuite(TestImageProcessing))
    test_suite.addTest(unittest.makeSuite(TestMetadataWrite))
    test_suite.addTest(unittest.makeSuite(TestFlacInfoExtraction))
    test_suite.addTest(unittest.makeSuite(TestIntegration))

    # 添加video_to_audio测试
    test_suite.addTest(unittest.makeSuite(TestVideoToAudio))

    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # 输出测试结果摘要
    print("\n" + "=" * 60)
    print("测试结果摘要")
    print("=" * 60)
    print(f"总测试数: {result.testsRun}")
    print(f"失败数: {len(result.failures)}")
    print(f"错误数: {len(result.errors)}")
    print(f"跳过数: {len(result.skipped)}")

    if result.failures:
        print("\n失败的测试:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")

    if result.errors:
        print("\n错误的测试:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")

    # 返回测试是否全部通过
    return len(result.failures) == 0 and len(result.errors) == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)