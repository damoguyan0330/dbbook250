# -8- coding = utf-8 -*-
# @Time : 2022/9/29 14:31
# @File : mypage.py
# @Software : PyCharm

class Pagination(object):
    def __init__(self, current_page, all_count, per_page_num=2, pager_count=11,q=None):
        """
        封装分页相关数据
        :param current_page: 当前页
        :param all_count:    数据库中的数据总条数
        :param per_page_num: 每页显示的数据条数
        :param pager_count:  最多显示的页码个数

        用法:
        queryset = model.objects.all()
        page_obj = Pagination(current_page,all_count)
        page_data = queryset[page_obj.start:page_obj.end]
        获取数据用page_data而不再使用原始的queryset
        获取前端分页样式用page_obj.page_html
        """
        try:
            current_page = int(current_page)
        except Exception as e:
            current_page = 1

        if current_page < 1:
            current_page = 1
        self.q = q
        self.current_page = current_page

        self.all_count = all_count
        self.per_page_num = per_page_num

        # 总页码
        all_pager, tmp = divmod(all_count, per_page_num)
        if tmp:
            all_pager += 1
        self.all_pager = all_pager

        self.pager_count = pager_count
        self.pager_count_half = int((pager_count - 1) / 2)

    @property
    def start(self):
        return (self.current_page - 1) * self.per_page_num

    @property
    def end(self):
        return self.current_page * self.per_page_num

    def page_html(self):
        # 如果总页码 < 11个：
        if self.all_pager <= self.pager_count:
            pager_start = 1
            pager_end = self.all_pager + 1
        # 总页码  > 11
        else:
            # 当前页如果<=页面上最多显示11/2个页码
            if self.current_page <= self.pager_count_half:
                pager_start = 1
                pager_end = self.pager_count + 1

            # 当前页大于5
            else:
                # 页码翻到最后
                if (self.current_page + self.pager_count_half) > self.all_pager:
                    pager_end = self.all_pager + 1
                    pager_start = self.all_pager - self.pager_count + 1
                else:
                    pager_start = self.current_page - self.pager_count_half
                    pager_end = self.current_page + self.pager_count_half + 1

        page_html_list = []
        # 添加前面的nav和ul标签
        if self.q:
            page_html_list.append('''
                                <nav aria-label='Page navigation>'
                                <ul class='pagination'>
                            ''')
            first_page = '<li><a href="?page=%s&q=%s">首页</a></li>' % (1,self.q)
            page_html_list.append(first_page)

            if self.current_page <= 1:
                prev_page = '<li class="disabled"><a href="#">上一页</a></li>'
            else:
                prev_page = '<li><a href="?page=%s&q=%s">上一页</a></li>' % (self.current_page - 1,self.q)

            page_html_list.append(prev_page)

            for i in range(pager_start, pager_end):
                if i == self.current_page:
                    temp = '<li class="active"><a href="?page=%s&q=%s">%s</a></li>' % (i,self.q, i,)
                else:
                    temp = '<li><a href="?page=%s&q=%s">%s</a></li>' % (i,self.q, i,)
                page_html_list.append(temp)

            if self.current_page >= self.all_pager:
                next_page = '<li class="disabled"><a href="#">下一页</a></li>'
            else:
                next_page = '<li><a href="?page=%s&q=%s">下一页</a></li>' % (self.current_page + 1,self.q)
            page_html_list.append(next_page)

            last_page = '<li><a href="?page=%s&q=%s">尾页</a></li>' % (self.all_pager,self.q)
            page_html_list.append(last_page)
            # 尾部添加标签
            page_html_list.append('''
                                                       </nav>
                                                       </ul>
                                                   ''')
        else:
            page_html_list.append('''
                        <nav aria-label='Page navigation>'
                        <ul class='pagination'>
                    ''')
            first_page = '<li><a href="?page=%s">首页</a></li>' % (1)
            page_html_list.append(first_page)

            if self.current_page <= 1:
                prev_page = '<li class="disabled"><a href="#">上一页</a></li>'
            else:
                prev_page = '<li><a href="?page=%s">上一页</a></li>' % (self.current_page - 1,)

            page_html_list.append(prev_page)

            for i in range(pager_start, pager_end):
                if i == self.current_page:
                    temp = '<li class="active"><a href="?page=%s">%s</a></li>' % (i, i,)
                else:
                    temp = '<li><a href="?page=%s">%s</a></li>' % (i, i,)
                page_html_list.append(temp)

            if self.current_page >= self.all_pager:
                next_page = '<li class="disabled"><a href="#">下一页</a></li>'
            else:
                next_page = '<li><a href="?page=%s">下一页</a></li>' % (self.current_page + 1,)
            page_html_list.append(next_page)

            last_page = '<li><a href="?page=%s">尾页</a></li>' % (self.all_pager,)
            page_html_list.append(last_page)
            # 尾部添加标签
            page_html_list.append('''
                                               </nav>
                                               </ul>
                                           ''')
        return ''.join(page_html_list)



# from urllib.parse import urlencode,quote,unquote
# class Pagination(object):
#     """
#     自定义分页
#     """
#     def __init__(self,current_page,total_count,base_url,params,per_page_count=10,max_pager_count=11):
#         try:
#             current_page = int(current_page)
#         except Exception as e:
#             current_page = 1
#         if current_page <=0:
#             current_page = 1
#         self.current_page = current_page
#         # 数据总条数
#         self.total_count = total_count
#
#         # 每页显示10条数据
#         self.per_page_count = per_page_count
#
#         # 页面上应该显示的最大页码
#         max_page_num, div = divmod(total_count, per_page_count)
#         if div:
#             max_page_num += 1
#         self.max_page_num = max_page_num
#
#         # 页面上默认显示11个页码（当前页在中间）
#         self.max_pager_count = max_pager_count
#         self.half_max_pager_count = int((max_pager_count - 1) / 2)
#
#         # URL前缀
#         self.base_url = base_url
#
#         # request.GET
#         import copy
#         params = copy.deepcopy(params)
#         # params._mutable = True
#         get_dict = params.to_dict()
#         # 包含当前列表页面所有的搜/索条件
#         # {source:[2,], status:[2], gender:[2],consultant:[1],page:[1]}
#         # self.params[page] = 8
#         # self.params.urlencode()
#         # source=2&status=2&gender=2&consultant=1&page=8
#         # href="/hosts/?source=2&status=2&gender=2&consultant=1&page=8"
#         # href="%s?%s" %(self.base_url,self.params.urlencode())
#         self.params = get_dict
#
#     @property
#     def start(self):
#         return (self.current_page - 1) * self.per_page_count
#
#     @property
#     def end(self):
#         return self.current_page * self.per_page_count
#
#     def page_html(self):
#         # 如果总页数 <= 11
#         if self.max_page_num <= self.max_pager_count:
#             pager_start = 1
#             pager_end = self.max_page_num
#         # 如果总页数 > 11
#         else:
#             # 如果当前页 <= 5
#             if self.current_page <= self.half_max_pager_count:
#                 pager_start = 1
#                 pager_end = self.max_pager_count
#             else:
#                 # 当前页 + 5 > 总页码
#                 if (self.current_page + self.half_max_pager_count) > self.max_page_num:
#                     pager_end = self.max_page_num
#                     pager_start = self.max_page_num - self.max_pager_count + 1   #倒这数11个
#                 else:
#                     pager_start = self.current_page - self.half_max_pager_count
#                     pager_end = self.current_page + self.half_max_pager_count
#
#         page_html_list = []
#         # {source:[2,], status:[2], gender:[2],consultant:[1],page:[1]}
#         # 首页
#         self.params['page'] = 1
#         first_page = '<li><a href="%s?%s">首页</a></li>' % (self.base_url,urlencode(self.params),)
#         page_html_list.append(first_page)
#         # 上一页
#         self.params["page"] = self.current_page - 1
#         if self.params["page"] < 1:
#             pervious_page = '<li class="disabled"><a href="%s?%s" aria-label="Previous">上一页</span></a></li>' % (self.base_url, urlencode(self.params))
#         else:
#             pervious_page = '<li><a href = "%s?%s" aria-label = "Previous" >上一页</span></a></li>' % ( self.base_url, urlencode(self.params))
#         page_html_list.append(pervious_page)
#         # 中间页码
#         for i in range(pager_start, pager_end + 1):
#             self.params['page'] = i
#             if i == self.current_page:
#                 temp = '<li class="active"><a href="%s?%s">%s</a></li>' % (self.base_url,urlencode(self.params), i,)
#             else:
#                 temp = '<li><a href="%s?%s">%s</a></li>' % (self.base_url,urlencode(self.params), i,)
#             page_html_list.append(temp)
#
#         # 下一页
#         self.params["page"] = self.current_page + 1
#         if self.params["page"] > self.max_page_num:
#             self.params["page"] = self.current_page
#             next_page = '<li class="disabled"><a href = "%s?%s" aria-label = "Next">下一页</span></a></li >' % (self.base_url, urlencode(self.params))
#         else:
#             next_page = '<li><a href = "%s?%s" aria-label = "Next">下一页</span></a></li>' % (self.base_url, urlencode(self.params))
#         page_html_list.append(next_page)
#
#         # 尾页
#         self.params['page'] = self.max_page_num
#         last_page = '<li><a href="%s?%s">尾页</a></li>' % (self.base_url, urlencode(self.params),)
#         page_html_list.append(last_page)
#
#         return ''.join(page_html_list)
